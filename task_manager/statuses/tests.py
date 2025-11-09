import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Status


@pytest.mark.django_db
class StatusCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.status = Status.objects.create(name='Test Status')
        self.user = User.objects.create_user(
            username='testuser',
            first_name='name',
            last_name='last_name',
            password='testpassword'
        )
        self.client.login(
            username='testuser',
            password='testpassword'
        )

    def test_status_create(self):
        response = self.client.post(
            reverse('status_create'),
            {
                'name': 'New Status'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_list(self):
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status.name)

    def test_status_update(self):
        response = self.client.post(
            reverse(
                'status_update',
                args=[self.status.id]
            ),
            {
                'name': 'Updated Status'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete(self):
        response = self.client.post(
            reverse(
                'status_delete',
                kwargs={'pk': self.status.id}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())
