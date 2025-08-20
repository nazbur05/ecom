from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Customer

class CustomerSignalTest(TestCase):
    def test_customer_created_on_user_creation(self):
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass123')
        self.assertTrue(hasattr(user, 'customer'), "Customer was not created for the user.")
        customer = Customer.objects.get(user=user)
        self.assertEqual(customer.user.username, "testuser")
        self.assertEqual(customer.user.email, "testuser@example.com")

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
