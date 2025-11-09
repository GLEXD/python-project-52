from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class UserCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            first_name='name',
            last_name='last_name',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_user_create(self):
        respone = self.client.post(reverse('user_create'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpassword',
            'password2': 'newpassword'
            }
        )
        self.assertEqual(respone.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_list(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_user_update(self):
        response = self.client.post(reverse(
            'user_update',
            args=[self.user.id]), {
                'username': 'updateduser',
                'first_name': 'Updated',
                'last_name': 'User',
                'password1': 'updatedpassword',
                'password2': 'updatedpassword'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_user_delete(self):
        response = self.client.post(reverse(
            'user_delete',
            kwargs={'pk': self.user.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())
