import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.tasks.models import Task

User = get_user_model()


@pytest.mark.django_db
class UserCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='user1',
            first_name='Name1',
            last_name='Last1',
            password='testpass123',
        )
        self.other_user = User.objects.create_user(
            username='user2',
            first_name='Name2',
            last_name='Last2',
            password='testpass123',
        )

    def test_user_create_success(self):
        url = reverse('user_create')
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpass123',
            'password2': 'newpass123',
        }
        resp = self.client.post(url, data)
        assert resp.status_code in (200, 302)
        assert User.objects.filter(username='newuser').exists()

    def test_user_create_password_mismatch(self):
        url = reverse('user_create')
        data = {
            'username': 'baduser',
            'first_name': 'B',
            'last_name': 'U',
            'password1': 'a',
            'password2': 'b',
        }
        resp = self.client.post(url, data)
        assert resp.status_code == 200
        assert not User.objects.filter(username='baduser').exists()

    def test_user_list_requires_login_and_shows_users(self):
        self.client.login(username='user1', password='testpass123')
        resp = self.client.get(reverse('user_list'))
        assert resp.status_code == 200
        assert self.user.username in resp.content.decode()

    def test_user_update_self_and_messages(self):
        self.client.login(username='user1', password='testpass123')
        url = reverse('user_update', kwargs={'pk': self.user.pk})
        data = {
            'username': 'updated_user1',
            'first_name': 'Updated',
            'last_name': 'Name',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        }
        resp = self.client.post(url, data, follow=True)
        assert resp.status_code in (200, 302)
        self.user.refresh_from_db()
        assert self.user.username == 'updated_user1'

        messages = list(get_messages(resp.wsgi_request))
        assert any('успеш' in str(m).lower() for m in messages)

    def test_user_update_other_is_blocked(self):
        self.client.login(username='user1', password='testpass123')
        url = reverse('user_update', kwargs={'pk': self.other_user.pk})
        data = {
            'username': 'boom',
            'first_name': 'X',
            'last_name': 'Y',
            'password1': 'aaaaaaaa',
            'password2': 'aaaaaaaa',
        }
        resp = self.client.post(url, data, follow=True)
        assert resp.status_code in (200, 302)

        messages = list(get_messages(resp.wsgi_request))
        assert any(
            'нет прав' in str(m).lower()
            or 'не авторизованы' in str(m).lower()
            or 'прав' in str(m).lower()
            for m in messages
        )

    def test_user_delete_self(self):
        self.client.login(username='user1', password='testpass123')
        url = reverse('user_delete', kwargs={'pk': self.user.pk})
        resp = self.client.post(url, follow=True)
        assert resp.status_code in (200, 302)
        assert not User.objects.filter(pk=self.user.pk).exists()

    def test_user_delete_other_blocked(self):
        self.client.login(username='user1', password='testpass123')
        url = reverse('user_delete', kwargs={'pk': self.other_user.pk})
        resp = self.client.post(url, follow=True)
        assert resp.status_code in (200, 302)
        assert User.objects.filter(pk=self.other_user.pk).exists()

        messages = list(get_messages(resp.wsgi_request))
        assert any(
            'нет прав' in str(m).lower() or 'прав' in str(m).lower()
            for m in messages
        )

    def test_user_delete_prevent_if_has_tasks(self):
        Task.objects.create(name='T1', author=self.other_user)
        self.client.login(username='user2', password='testpass123')
        url = reverse('user_delete', kwargs={'pk': self.other_user.pk})
        resp = self.client.post(url, follow=True)
        assert resp.status_code in (200, 302)
        assert User.objects.filter(pk=self.other_user.pk).exists()

        messages = list(get_messages(resp.wsgi_request))
        assert any(
            'нет прав' in str(m).lower() or 'прав' in str(m).lower()
            for m in messages
        )
