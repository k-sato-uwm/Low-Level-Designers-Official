from django.test import TestCase
from scheduler.models import Course, User
from ManagerClasses.LoginManager import LoginManager

class LoginManagerTests(TestCase):
    def setUp(self):
        user = User(username="test_user", password="securepassword", role="Teaching Assistant")
        user.save()

    def test_login_manager_valid_credentials(self):
        """Test the LoginManager's verify_credentials method with valid credentials."""
        result = LoginManager.verify_credentials('test_user', 'securepassword')
        self.assertIsNotNone(result)
        self.assertEqual(result['user'].username, 'test_user')


    def test_login_manager_invalid_credentials(self):
        """Test the LoginManager's verify_credentials method with invalid credentials."""
        result = LoginManager.verify_credentials('test_user', 'wrongpassword')
        self.assertEqual(result['success'], False)


    def test_login_manager_nonexistent_user(self):
        """Test the LoginManager's verify_credentials method with nonexistent user."""
        result = LoginManager.verify_credentials('nonexistent_user', 'securepassword')
        self.assertEqual(result['success'], False)