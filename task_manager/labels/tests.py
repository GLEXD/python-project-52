from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Label


# Create your tests here.
class LabelCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(
            username='testuser',
            password='testpassword'
        )

    def test_label_list_view(self):
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'label_list.html')

    def test_label_create_view(self):
        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'label_form.html')

    def test_label_update_view(self):
        label = Label.objects.create(name='Test Label')
        response = self.client.post(
            reverse(
                'label_update',
                args=[label.pk]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'label_form.html'
        )

    def test_label_delete_view(self):
        label = Label.objects.create(name='Test Label')
        response = self.client.post(
            reverse(
                'label_delete',
                args=[label.pk]
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=label.pk).exists())
