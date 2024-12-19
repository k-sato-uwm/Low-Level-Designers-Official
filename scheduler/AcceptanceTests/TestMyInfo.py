from django.test import TestCase, Client
from scheduler.models import *

class MyInfoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/myinfo/'

        # Create test instructor and course
        self.usertest = User.objects.create(username="test_me",
                                        password='pass123',
                                        role="Teaching Assistant",
                                        email='test.user@uwm.edu',
                                        phone_number='414-123-4567',
                                        address='2200 E Kenwood Blvd')
        self.course = Course.objects.create(
            course_code="CS101",
            course_name="Intro to Computer Science",
            # instructor=self.instructor
        )

        self.assignment = Assignments.objects.create(user=self.usertest, course=self.course)

    def test_myInfoLoggedIn(self):
        self.client.post('/', {'username': 'test_me', 'password': 'pass123'}, follow=True)
        self.assertEqual(self.client.session['username'], 'test_me')
        self.assertEqual(self.client.session['role'], 'Teaching Assistant')
        res2 = self.client.get(self.url, follow=True)
        self.assertEqual(res2.status_code, 200)
        self.assertTemplateUsed(res2, template_name='MyInfo.html')
        self.assertEqual(res2.context['user'], self.usertest, msg='Displaying wrong user!')

    def test_myInfoNotLoggedIn(self):
        res = self.client.get(self.url, follow=True)
        self.assertRedirects(res, '/', 302)

    def test_myInfoEditEmail(self):
        self.client.post('/', {'username': 'test_me', 'password': 'pass123'}, follow=True)
        self.assertEqual(self.client.session['username'], 'test_me')
        self.assertEqual(self.client.session['role'], 'Teaching Assistant')
        res = self.client.post(self.url, {'email':'new.mail@gmail.com'})
        self.assertEqual(res.status_code, 200)
        user = User.objects.get(username=self.client.session['username'])
        self.assertEqual(user.email, 'new.mail@gmail.com', msg='Email not updated!')

    def test_myInfoEditPhone(self):
        self.client.post('/', {'username': 'test_me', 'password': 'pass123'}, follow=True)
        self.assertEqual(self.client.session['username'], 'test_me')
        self.assertEqual(self.client.session['role'], 'Teaching Assistant')
        res = self.client.post(self.url, {'phone_number':'1234567890'})
        self.assertEqual(res.status_code, 200)
        user = User.objects.get(username=self.client.session['username'])
        self.assertEqual(user.phone_number, '1234567890', msg='Number not updated!')

    def test_myInfoEditBoth(self):
        self.client.post('/', {'username': 'test_me', 'password': 'pass123'}, follow=True)
        self.assertEqual(self.client.session['username'], 'test_me')
        self.assertEqual(self.client.session['role'], 'Teaching Assistant')
        res = self.client.post(self.url, {'email':'new.mail@gmail.com', 'phone_number':'1234567890'})
        self.assertEqual(res.status_code, 200)
        user = User.objects.get(username=self.client.session['username'])
        self.assertEqual(user.email, 'new.mail@gmail.com', msg='Email not updated!')
        self.assertEqual(user.phone_number, '1234567890', msg='Number not updated!')