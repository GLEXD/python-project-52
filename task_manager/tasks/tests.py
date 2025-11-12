import pytest
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from task_manager.statuses.models import Status

from .filters import TaskFilter
from .models import Task


@pytest.mark.django_db
class TaskViewAndFilterTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='author', password='pw')
        self.other = User.objects.create_user(username='other', password='pw')
        self.status = Status.objects.create(name='S1')
        self.task1 = Task.objects.create(
            name='Task 1',
            author=self.user,
            description='d1',
            status=self.status,
        )
        self.task2 = Task.objects.create(
            name='Task 2',
            author=self.other,
            description='d2',
            status=self.status,
        )
        self.client.login(username='author', password='pw')

    def test_task_list_and_create_and_detail(self):
        resp = self.client.get(reverse('task_list'))
        assert resp.status_code == 200

        resp = self.client.post(
            reverse('task_create'),
            {
                'name': 'Created',
                'description': 'xx',
                'status': self.status.id,
            },
            follow=True,
        )
        assert resp.status_code in (200, 302)
        assert Task.objects.filter(name='Created').exists()

    def test_task_update_by_author(self):
        url = reverse('task_update', args=[self.task1.id])
        resp = self.client.post(
            url,
            {
                'name': 'Task 1 updated',
                'description': 'updated',
                'status': self.status.id,
            },
            follow=True,
        )
        assert resp.status_code in (200, 302)
        self.task1.refresh_from_db()
        assert self.task1.name == 'Task 1 updated'

        messages = list(get_messages(resp.wsgi_request))
        assert any('успеш' in str(m).lower() for m in messages)

    def test_task_update_by_non_author_is_blocked(self):
        self.client.logout()
        self.client.login(username='other', password='pw')
        url = reverse('task_update', args=[self.task1.id])

        resp = self.client.post(
            url,
            {'name': 'BadUpdate', 'description': 'x'},
            follow=True,
        )
        assert resp.status_code in (200, 302)
        self.task1.refresh_from_db()
        assert self.task1.name != 'BadUpdate'

        messages = list(get_messages(resp.wsgi_request))
        assert any(
            'не можете' in str(m).lower()
            or 'нет прав' in str(m).lower()
            for m in messages
        )

    def test_task_delete_by_non_author_blocked(self):
        self.client.logout()
        self.client.login(username='other', password='pw')
        url = reverse('task_delete', kwargs={'pk': self.task1.id})

        resp = self.client.post(url, follow=True)
        assert resp.status_code in (200, 302)
        assert Task.objects.filter(pk=self.task1.pk).exists()

        messages = list(get_messages(resp.wsgi_request))
        assert any(
            'автор' in str(m).lower() or 'удалить' in str(m).lower()
            for m in messages
        )

    def test_task_delete_by_author(self):
        url = reverse('task_delete', kwargs={'pk': self.task1.id})
        resp = self.client.post(url, follow=True)
        assert resp.status_code in (200, 302)
        assert not Task.objects.filter(pk=self.task1.pk).exists()

        messages = list(get_messages(resp.wsgi_request))
        assert any('успеш' in str(m).lower() for m in messages)

    def test_taskfilter_self_tasks_true_returns_only_user_tasks(self):
        request = self.factory.get('/?self_tasks=1')
        request.user = self.user
        qs = Task.objects.all()

        f = TaskFilter({'self_tasks': '1'}, queryset=qs, request=request)
        res_pks = list(f.qs.values_list('pk', flat=True))

        assert self.task1.pk in res_pks
        assert self.task2.pk not in res_pks

    def test_taskfilter_executor_label_from_instance(self):
        request = self.factory.get('/')
        request.user = self.user
        qs = Task.objects.all()

        f = TaskFilter({}, queryset=qs, request=request)
        assert 'executor' in f.form.fields
