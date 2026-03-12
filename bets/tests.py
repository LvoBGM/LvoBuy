from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .views import NewListingForm
from .models import Listing

# Create your tests here.
class AccessTests(TestCase):

    def setUp(self):
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.new_listing_url = reverse('new_listing')
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
    
    def test_anonymous_user_redirected_from_new_listing(self):
        """Anonymous users will be redirected when accessings new listing page."""
        response = self.client.get(self.new_listing_url)

        expected_url = f"{self.login_url}?next={self.new_listing_url}"
        self.assertRedirects(response, expected_url)
    
    def test_logged_in_user_can_access_new_listing(self):
        """Logged in users can access new listing page."""
        self.client.login(username='testuser', password='krastavica')

        response = self.client.get(self.new_listing_url)

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


class TestNewListingForm(TestCase):

    def test_form_is_valid_with_all_fields(self):
        """Test that the form is valid when all fields are provided correctly"""
        data = {
            'title': 'Vintage Camera',
            'description': 'A beautiful 1950s film camera.',
            'image_url': 'https://example.com/image.jpg',
            'starting_bid': 50.00
        }
        form = NewListingForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_is_valid_without_image_url(self):
        """Test that the form is still valid if image_url is missing"""
        data = {
            'title': 'Vintage Camera',
            'description': 'A beautiful 1950s film camera.',
            'image_url': '',
            'starting_bid': 50.00
        }
        form = NewListingForm(data=data)
        self.assertTrue(form.is_valid(), msg="The form should be valid even without an image URL.")

    def test_form_is_invalid_without_required_fields(self):
        """Test that the form fails if required fields are missing"""

        # No title
        data = {
            'title': '', 
            'description': 'Missing a title here!',
            'starting_bid': 10.00
        }
        form = NewListingForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

        # No description
        data = {
            'title': 'Title', 
            'description': '',
            'starting_bid': 10.00
        }
        form = NewListingForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)
        
        # No Bid
        data = {
            'title': 'Title', 
            'description': 'No bid',
        }
        form = NewListingForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('starting_bid', form.errors)

    def test_post_create_listing_fails_for_guest(self):
        """Test that a non-logged-in user cannot create a listing via POST"""

        self.new_listing_url = reverse('new_listing') 

        data = {
            'title': 'Stolen Goods',
            'description': 'I am not logged in!',
            'starting_bid': 100.00
        }
        response = self.client.post(self.new_listing_url, data=data)

        # Ensure redirect happens instead of creation
        self.assertEqual(response.status_code, 302)

        # Ensure the listing was NOT actually created in the database
        self.assertEqual(Listing.objects.count(), 0)