from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.
class AccessTests(TestCase):

    def setUp(self):
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.home_url = reverse('home_specific_page', args=[1])

        self.user = User.objects.create_user(
            username='testuser',
            password='krastavica'
        )
    
    def test_anonymous_user_can_access_login(self):
        """Anonymous users can access login page."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_can_access_register(self):
        """Anonymous users can access register page."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_redirected_from_login(self):
        """Logged in users will be redirected when accessing login page"""
        self.client.login(username='testuser', password='krastavica')

        response = self.client.get(self.login_url)

        self.assertRedirects(response, self.home_url)

    def test_logged_in_user_redirected_from_register(self):
        """Logged in users will be redirected when accessing register page"""
        self.client.login(username='testuser', password='krastavica')

        response = self.client.get(self.register_url)

        self.assertRedirects(response, self.home_url)