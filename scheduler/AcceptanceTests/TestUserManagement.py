from django.test import TestCase, Client
from django.urls import reverse
from scheduler.models import Course, User
from django.db import transaction, IntegrityError
from ManagerClasses.userManager import UserManagement
from django.contrib.messages import get_messages


class UserManagementAcceptanceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('UserManagement')

        # Initialize the UserManagement instance
        self.user_management = UserManagement()

        # Create initial data
        self.duplicate_user = User.objects.create(
            username="test_user",
            role=User.SUPERVISOR,
            email="test_user@example.com",
            phone_number="9876543210",
            address="456 Duplicate Lane",
            password="password123"
        )

        # Create a duplicate user for testing
        self.existing_user = User.objects.create(
            username="existing_user",
            role=User.INSTRUCTOR,
            email="existing@example.com",
            phone_number="1234567890",
            address="123 Test Lane",
            password="password123"
        )

    def test_get_user_management_page(self):
        # Test that the GET request returns the correct template and status code
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_management.html')

        # Test that the context includes users
        self.assertIn('users', response.context)
        self.assertTrue(len(response.context['users']) > 0)


    def test_create_supervisor_success(self):
        data = {
            'action': 'add',
            'role': User.SUPERVISOR,
            'username': 'new_user',
            'email': 'new_user@example.com',
            'phone_number': '9876543210',
            'address': '456 New Street',
            'password': 'securepassword'
        }
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='new_user').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Supervisor new_user added successfully!', str(messages[0]))

    def test_create_TA_success(self):
        data = {
            'action': 'add',
            'role': User.TEACHING_ASSISTANT,
            'username': 'new_user',
            'email': 'new_user@example.com',
            'phone_number': '9876543210',
            'address': '456 New Street',
            'password': 'securepassword'
        }
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='new_user').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Teaching Assistant new_user added successfully!', str(messages[0]))

    def test_create_Instructor_success(self):
        data = {
            'action': 'add',
            'role': User.INSTRUCTOR,
            'username': 'new_user',
            'email': 'new_user@example.com',
            'phone_number': '9876543210',
            'address': '456 New Street',
            'password': 'securepassword'
        }
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='new_user').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Instructor new_user added successfully!', str(messages[0]))


    def test_create_user_duplicate(self):
        entry = {
            'username': 'existing_user',
            'role': User.INSTRUCTOR,
            'email': 'duplicate@example.com',
            'phone_number': '9876543210',
            'address': '123 Duplicate Lane',
            'password': 'password123'
        }
        try:
            with transaction.atomic():
                result = self.user_management.create(entry)
                self.assertFalse(result['success'], "Duplicate user creation should fail.")
        except IntegrityError:
            pass

    def test_update_user_success(self):
        data = {
            'action': 'edit',
            'id': self.existing_user.user_id,
            'username': 'updated_user',
            'role': User.SUPERVISOR,
            'email': 'updated_user@example.com',
            'phone_number': '9876543211',
            'address': 'Updated Address',
            'password': 'updatedpassword'
        }
        response = self.client.post(self.url, data, follow=True)


        self.assertEqual(response.status_code, 200)


        updated_user = User.objects.get(user_id=self.existing_user.user_id)
        self.assertEqual(updated_user.username, 'updated_user')


        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('User updated successfully!' in str(message) for message in messages))

    def test_delete_user_success(self):
        data = {
            'action': 'delete',
            'id': self.existing_user.user_id
        }
        response = self.client.post(self.url, data, follow=True)


        self.assertEqual(response.status_code, 200)


        self.assertFalse(User.objects.filter(user_id=self.existing_user.user_id).exists())


        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('User deleted successfully!' in str(message) for message in messages))

    def test_delete_nonexistent_user(self):
        data = {
            'action': 'delete',
            'id': 99999
        }
        response = self.client.post(self.url, data, follow=True)


        self.assertEqual(response.status_code, 200)


        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('User does not exist!' in str(message) for message in messages))

    def test_invalid_action(self):

        data = {
            'action': 'invalid_action'
        }
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Invalid action specified.', str(messages[0]))