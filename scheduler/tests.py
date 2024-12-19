from django.test import TestCase, Client
from django.urls import reverse
from scheduler.models import Course, User
from django.db import transaction, IntegrityError
from ManagerClasses.userManager import UserManagement
from django.contrib.messages import get_messages

# pageload, blank, and invalid username passing
class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('login')
        user = User(username="test_user", password="securepassword", role="Teaching Assistant")
        user.save()

    def test_login_page_loads(self):
        """Test that the login page loads successfully via GET."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_successful(self):
        """Test a successful login with valid credentials."""

        data = {'username': 'test_user', 'password': 'securepassword'}
        response = self.client.post('/', {'username': 'test_user', 'password': "securepassword"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/dashboard/', 302)  # Redirect after successful login
        self.assertEqual(self.client.session['username'], 'test_user')  # Check session

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
        self.assertEqual(str(messages[0]), "User not found.")

    def test_login_redirect(self):
        """Test redirection based on user role."""
        data = {'username': 'test_user', 'password': 'securepassword'}
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/dashboard/', 302)

    def test_login_session_data(self):
        """Test that user data is correctly stored in session upon login."""
        data = {'username': 'test_user', 'password': 'securepassword'}
        self.client.post(self.url, data)
        self.assertEqual(self.client.session['username'], 'test_user')

class DashboardTests(TestCase):
    def setUp(self):
        self.client = Client()

        ta = User(username='TestTA', password='pass123', role='Teaching Assistant')
        ta.save()
        inst = User(username='TestInst', password='pass123', role='Instructor')
        inst.save()
        admin = User(username='TestAdmin', password='pass123', role='Supervisor')
        admin.save()

    def test_signedinAdmin(self): # If the user signs in as a Supervisor
        res = self.client.post('/', {'username': 'TestAdmin', 'password': 'pass123'}, follow=True)
        self.assertEqual(self.client.session['username'], 'TestAdmin')
        self.assertEqual(self.client.session['role'], 'Supervisor')
        self.assertRedirects(res, '/dashboard/', 302)
        self.assertTemplateUsed(res, template_name='SupervisorDash.html')
        self.assertEqual(res.context['name'], 'TestAdmin')

    def test_signedinInstructor(self): # If the user signs in as an Instructor
        res = self.client.post('/', {'username': 'TestInst', 'password': 'pass123'}, follow=True)
        self.assertEqual(self.client.session['username'], 'TestInst')
        self.assertEqual(self.client.session['role'], 'Instructor')
        self.assertRedirects(res, '/dashboard/', 302)
        self.assertTemplateUsed(res, template_name='InstDash.html')
        self.assertEqual(res.context['name'], 'TestInst')

    def test_signedinTA(self): # If the user signs in as a TA
        res = self.client.post('/', {'username': 'TestTA', 'password': 'pass123'}, follow=True)
        self.assertEqual(self.client.session['username'], 'TestTA')
        self.assertEqual(self.client.session['role'], 'Teaching Assistant')
        self.assertRedirects(res, '/dashboard/', 302)
        self.assertTemplateUsed(res, template_name='TADash.html')
        self.assertEqual(res.context['name'], 'TestTA')

    def test_notsignedin(self): # If the user is not signed in
        res = self.client.get('/dashboard/', follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertRedirects(res, '/', 302)

    def test_postrequest(self): # POST requests should not be sent to Dashboard page
        with self.assertRaises(NotImplementedError):
            res = self.client.post('/dashboard/', data={'data': 'BAD'}, follow=True)

class CourseManagementTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('course_management')

        # Create test instructor and course
        self.instructor = User.objects.create(username="test_instructor", role="Instructor")
        self.course = Course.objects.create(
            course_code="CS101",
            course_name="Intro to Computer Science",
            instructor=self.instructor
        )

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'CourseManagement.html')
        self.assertIn('courses', response.context)
        self.assertIn('instructors', response.context)

    def test_post_add_course_success(self):
        data = {
            'add_course': '',
            'course_code': 'CS102',
            'course_name': 'Advanced Computer Science',
            'instructor_name': 'test_instructor'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Course.objects.filter(course_code="CS102").exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Course added successfully.")

    def test_post_add_course_duplicate(self):
        data = {
            'add_course': '',
            'course_code': 'CS101',  # Duplicate code
            'course_name': 'Duplicate Course',
            'instructor_name': 'test_instructor'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Failed to add course. It may already exist, or the instructor was not found.")

    def test_post_add_course_missing_fields(self):
        data = {
            'add_course': '',
            'course_code': 'CS103',
            'course_name': ''  # Missing course name
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "All fields are required to add a course.")

    def test_post_delete_course_success(self):
        data = {
            'delete_course': '',
            'course_id': self.course.course_id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertFalse(Course.objects.filter(course_id=self.course.course_id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Course deleted successfully.")

    def test_post_delete_course_invalid_id(self):
        data = {
            'delete_course': '',
            'course_id': 999  # Nonexistent course ID
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Failed to delete course. Course may not exist.")

    def test_post_edit_course_success(self):
        data = {
            'edit_course': '',
            'course_id': self.course.course_id,
            'instructor_name': 'test_instructor'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect
        updated_course = Course.objects.get(course_id=self.course.course_id)
        self.assertEqual(updated_course.instructor.username, 'test_instructor')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Course updated successfully.")

    def test_post_edit_course_invalid_id(self):
        data = {
            'edit_course': '',
            'course_id': 999,  # Nonexistent course ID
            'instructor_name': 'test_instructor'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Failed to update course. Instructor or course may not exist.")

    def test_post_edit_course_missing_fields(self):
        data = {
            'edit_course': '',
            'course_id': self.course.course_id,
            'instructor_name': ''  # Missing instructor name
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Course ID and Instructor name are required to update.")


###
    def test_create_course_invalid_instructor_name(self):
        data = {
            'add_course': '',
            'course_code': 'CS104',
            'course_name': 'Whatever',
            'instructor_name': 'invalid$instructor#name!'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         "Failed to add course. It may already exist, or the instructor was not found.")

    def test_stress_add_multiple_courses(self):
        #populate db
        for i in range(100):
            data = {
                'add_course': '',
                'course_code': f'CS{i + 200}',
                'course_name': f'Course {i + 200}',
                'instructor_name': 'test_instructor'
            }
            response = self.client.post(self.url, data)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(Course.objects.filter(course_code=f'CS{i + 200}').exists())

    def test_delete_course_missing_id(self):
        data = {
            'delete_course': ''  # No course_id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Course ID is required to delete.")

    def test_edit_nonexistent_course(self):
        data = {
            'edit_course': '',
            'course_id': 999,  # Nonexistent course ID
            'instructor_name': 'test_instructor'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Failed to update course. Instructor or course may not exist.")
        # Ensure existing courses are unaffected
        self.assertTrue(Course.objects.filter(course_code='CS101').exists())

    def test_concurrent_edit_and_delete(self):
        data_edit = {
            'edit_course': '',
            'course_id': self.course.course_id,
            'instructor_name': 'test_instructor'
        }
        data_delete = {
            'delete_course': '',
            'course_id': self.course.course_id
        }

        # Edit course
        response_edit = self.client.post(self.url, data_edit)
        self.assertEqual(response_edit.status_code, 302)

        # Delete course
        response_delete = self.client.post(self.url, data_delete)
        self.assertEqual(response_delete.status_code, 302)

        # Ensure course is deleted
        self.assertFalse(Course.objects.filter(course_id=self.course.course_id).exists())

    def test_edit_course_nonexistent_instructor(self):
        data = {
            'edit_course': '',
            'course_id': self.course.course_id,
            'instructor_name': 'nonexistent_instructor'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Failed to update course. Instructor or course may not exist.")

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

    def test_create_user_success(self):
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
