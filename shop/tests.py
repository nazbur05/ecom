from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Customer, Product, Order, Category, SubCategory

class CustomerSignalTest(TestCase):
    def test_customer_created_on_user_creation(self):
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass123')
        self.assertTrue(hasattr(user, 'customer'), "Customer was not created for the user.")
        customer = Customer.objects.get(user=user)
        self.assertEqual(customer.user.username, "testuser")
        self.assertEqual(customer.user.email, "testuser@example.com")

class SignupViewTest(TestCase):
    def test_signup_success(self):
        response = self.client.post(
            '/shop/signup/', {
                'username': 'testuser',
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'testuser@example.com',
                'password1': 'testpass123',
                'password2': 'testpass123'
            }
        )
        self.assertRedirects(response, '/shop/')
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

class FavouritesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='favuser', email='favuser@example.com', password='testpass123')
        self.customer = Customer.objects.get(user=self.user)
        self.category = Category.objects.create(name='Test Category')
        self.subcategory = SubCategory.objects.create(name='Test Sub', parent=self.category)
        self.product = Product.objects.create(
            name='Test Product',
            price=1000,
            subcategory=self.subcategory
        )

    def test_add_to_favourites(self):
        self.client.login(username='favuser', password='testpass123')
        url = f'/shop/api/customers/{self.customer.id}/add_favourite/'
        response = self.client.post(
            url,
            {'product_id': self.product.id},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.customer.refresh_from_db()
        self.assertIn(self.product, self.customer.favourites.all())

    def test_remove_from_favourites(self):
        self.customer.favourites.add(self.product)
        self.client.login(username='favuser', password='testpass123')
        url = f'/shop/api/customers/{self.customer.id}/remove_favourite/'
        response = self.client.post(
            url,
            {'product_id': self.product.id},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.customer.refresh_from_db()
        self.assertNotIn(self.product, self.customer.favourites.all())

class OrderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='orderuser',
            email='orderuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.customer = Customer.objects.get(user=self.user)
        self.category = Category.objects.create(name='Order Category')
        self.subcategory = SubCategory.objects.create(name='Order Sub', parent=self.category)
        self.product = Product.objects.create(
            name='Order Product',
            price=1500,
            subcategory=self.subcategory
        )
        self.customer.phone = '+48123456789'
        self.customer.save()

    def test_place_order(self):
        self.client.login(username='orderuser', password='testpass123')
        add_to_cart_url = f'/shop/api/customers/{self.customer.id}/add_to_cart/'
        self.client.post(
            add_to_cart_url,
            {'product_id': self.product.id},
            content_type='application/json'
        )
        checkout_url = f'/shop/api/customers/{self.customer.id}/checkout/'
        response = self.client.post(
            checkout_url,
            {'address': 'Test Address', 'phone': '+48123456789'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.filter(customer=self.customer, product=self.product, status=True).exists())
