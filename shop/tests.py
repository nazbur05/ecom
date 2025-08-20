from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class SignupViewTest(TestCase):
    def test_signup_success(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_signup_password_mismatch(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password1': 'testpass123',
            'password2': 'wrongpass',
        })
        self.assertContains(response, 'Passwords do not match.')

    def test_signup_duplicate_email(self):
        User.objects.create_user(username='existinguser', email='existing@example.com', password='pass')
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertContains(response, 'Email is already in use.')
