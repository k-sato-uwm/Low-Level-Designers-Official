import unittest

from manager.LoginManager import LoginManager


class MyTestCase(unittest.TestCase):
    def test_login_manager_valid_credentials(self):
        """Test the LoginManager's verify_credentials method with valid credentials."""
        result = LoginManager.verify_credentials('test_user', 'securepassword')
        self.assertIsNotNone(result)
        self.assertEqual(result.username, 'test_user')

    def test_login_manager_invalid_credentials(self):
        """Test the LoginManager's verify_credentials method with invalid credentials."""
        result = LoginManager.verify_credentials('test_user', 'wrongpassword')
        self.assertIsNone(result)

    def test_login_manager_nonexistent_user(self):
        """Test the LoginManager's verify_credentials method with nonexistent user."""
        result = LoginManager.verify_credentials('nonexistent_user', 'securepassword')
        self.assertIsNone(result)




