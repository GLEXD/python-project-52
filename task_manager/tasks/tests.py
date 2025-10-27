from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Task


class TaskViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            first_name='name',
            last_name='last_name',
            password='testpassword'
        )
        self.task = Task.objects.create(
            name='Test Task',
            author=self.user,
            description='This is a test task.',
        )
        self.client.login(username='testuser', password='testpassword')

    def test_task_create(self):
        response = self.client.post(
            reverse('task_create'),
            {
                'name': 'New Task',
                'author': self.user,
                'description': 'This is a new task.',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_list(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_update(self):
        response = self.client.post(
            reverse('task_update', args=[self.task.id]),
            {
                'name': 'Updated Task',
                'description': 'This task has been updated.',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_task_delete(self):
        response = self.client.post(
            reverse('task_delete', kwargs={'pk': self.task.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())