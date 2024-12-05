from django.test import TestCase
from manager.userManager import UserManagement
from scheduler.models import User


class UserManagementTests(TestCase):
    def setUp(self):

        self.user_management = UserManagement()
        self.test_user = User.objects.create(
            username="test_user",
            role=User.INSTRUCTOR,
            email="test_user@example.com",
            phone_number="1234567890",
            address="123 Test Street",
            password="testpassword"
        )

    def test_create_user_success(self):

        entry = {
            'username': 'new_user',
            'role': User.TEACHING_ASSISTANT,
            'email': 'new_user@example.com',
            'phone_number': '9876543210',
            'address': '456 New Lane',
            'password': 'securepassword'
        }
        result = self.user_management.create(entry)
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], f"{entry['role']} {entry['username']} added successfully!")
        self.assertTrue(User.objects.filter(username=entry['username']).exists())

    def test_create_user_duplicate(self):

        entry = {
            'username': 'test_user',
            'role': User.SUPERVISOR,
            'email': 'duplicate@example.com',
            'phone_number': '1112223333',
            'address': '789 Duplicate Ave',
            'password': 'password'
        }
        result = self.user_management.create(entry)
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'User already exists!')


    def test_update_user(self):

        user_id = self.test_user.user_id
        entry = {
            'username': 'updated_user',
            'role': User.TEACHING_ASSISTANT,
            'email': 'updated_user@example.com',
            'phone_number': '1112223334',
            'address': 'Updated Address',
            'password': 'updatedpassword'
        }
        result = self.user_management.update(user_id, entry)
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'User updated successfully!')
        updated_user = User.objects.get(pk=user_id)
        self.assertEqual(updated_user.username, entry['username'])
        self.assertEqual(updated_user.email, entry['email'])

    def test_update_user_nonexistent(self):

        user_id = 99999
        entry = {
            'username': 'nonexistent_user',
            'role': User.TEACHING_ASSISTANT,
            'email': 'nonexistent_user@example.com',
            'phone_number': '1112223334',
            'address': 'Nonexistent Address',
            'password': 'nonexistentpassword'
        }
        result = self.user_management.update(user_id, entry)
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'User does not exist!')

    def test_delete_user_success(self):

        user_id = self.test_user.user_id
        result = self.user_management.delete(user_id)
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'User deleted successfully!')
        self.assertFalse(User.objects.filter(pk=user_id).exists())

    def test_delete_user_nonexistent(self):

        user_id = 99999
        result = self.user_management.delete(user_id)
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'User does not exist!')
