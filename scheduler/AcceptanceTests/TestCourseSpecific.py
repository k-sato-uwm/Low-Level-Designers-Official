from django.test import TestCase, Client
from django.urls import reverse
from scheduler.models import Course, User
from django.contrib.messages import get_messages
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