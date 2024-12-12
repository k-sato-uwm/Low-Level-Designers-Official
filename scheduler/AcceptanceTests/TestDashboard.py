from django.test import TestCase, Client
from scheduler.models import Course, User

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