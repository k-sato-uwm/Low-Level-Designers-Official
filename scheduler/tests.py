from django.test import TestCase, Client
from django.urls import reverse
from .models import User
from manager.LoginManager import LoginManager
from django.contrib.messages import get_messages


class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('login')
        user = User(username="test_user", password="securepassword", role="TA")
        user.save()

    def test_login_page_loads(self):
        """Test that the login page loads successfully via GET."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_successful(self):
        """Test a successful login with valid credentials."""
        data = {'username': 'test_user', 'password': 'securepassword'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertEqual(response.url, '/dashboard/')  # Redirect based on role
        self.assertIn('_auth_user_id', self.client.session)  # Check session

    def test_login_invalid_username(self):
        """Test login with a nonexistent username."""
        data = {'username': 'nonexistent_user', 'password': 'securepassword'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "User not found.")

    def test_login_invalid_password(self):
        """Test login with a valid username but incorrect password."""
        data = {'username': 'test_user', 'password': 'wrongpassword'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Incorrect password.")

    def test_login_blank_fields(self):
        """Test login with blank username and password."""
        data = {'username': '', 'password': ''}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "User not found.")

    def test_login_edge_case_long_username(self):
        """Test login with an excessively long username."""
        data = {'username': 'a' * 256, 'password': 'securepassword'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Invalid username or password.")

    def test_login_role_redirect(self):
        """Test redirection based on user role."""
        self.user.role = "Admin"
        self.user.save()
        data = {'username': 'test_user', 'password': 'securepassword'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')

    def test_login_session_data(self):
        """Test that user data is correctly stored in session upon login."""
        data = {'username': 'test_user', 'password': 'securepassword'}
        self.client.post(self.url, data)
        self.assertEqual(self.client.session['username'], 'test_user')

    # def test_logout_user(self):
    #     """Test the logout functionality."""
    #     # Login the user first
    #     self.client.post(self.url, {'username': 'test_user', 'password': 'securepassword'})
    #     response = self.client.get(reverse('logout'))  # Assuming logout URL is named 'logout'
    #     self.assertEqual(response.status_code, 302)  # Redirect after logout
    #     self.assertNotIn('_auth_user_id', self.client.session)  # Session should be cleared

    # def test_concurrent_login_attempts(self):
    #     """Test handling of multiple simultaneous login attempts."""
    #     for _ in range(10):  # Simulate 10 login attempts
    #         data = {'username': 'test_user', 'password': 'securepassword'}
    #         response = self.client.post(self.url, data)
    #         self.assertEqual(response.status_code, 302)
    #         self.assertEqual(response.url, '/ta_dashboard/')

    # def test_login_manager_valid_credentials(self):
    #     """Test the LoginManager's verify_credentials method with valid credentials."""
    #     result = LoginManager.verify_credentials('test_user', 'securepassword')
    #     self.assertIsNotNone(result)
    #     self.assertEqual(result.username, 'test_user')
    #
    # def test_login_manager_invalid_credentials(self):
    #     """Test the LoginManager's verify_credentials method with invalid credentials."""
    #     result = LoginManager.verify_credentials('test_user', 'wrongpassword')
    #     self.assertIsNone(result)
    #
    # def test_login_manager_nonexistent_user(self):
    #     """Test the LoginManager's verify_credentials method with nonexistent user."""
    #     result = LoginManager.verify_credentials('nonexistent_user', 'securepassword')
    #     self.assertIsNone(result)
