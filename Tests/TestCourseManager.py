from django.test import TestCase
from scheduler.models import Course, User
from ManagerClasses.CourseManager import *


class TestCourseManager(TestCase):
    def setUp(self):
        # create a test instructor
        self.instructor = User.objects.create(username="test_instructor", user_id=1)
        self.user2=User.objects.create(username='test_user2', user_id=2)
        # create a test course
        self.course = Course.objects.create(
            course_code="CS101",
            course_name="Intro to Computer Science",
        )
        self.assignment = Assignments.objects.create(user=self.instructor, course=self.course)
        self.assignment2 = Assignments.objects.create(user=self.user2, course=self.course)

#create() Tests
    def test_create_successful(self):
        entry = {
            "course_code": "CS102",
            "course_name": "Advanced Computer Science",
            "instructor_name": "test_instructor"
        }
        result = CourseManager.create(entry)
        self.assertTrue(result)
        self.assertTrue(Course.objects.filter(course_code="CS102").exists())

    def test_create_duplicate_course(self):
        entry = {
            "course_code": "CS101",
            "course_name": "Intro to Computer Science",
            "instructor_name": "test_instructor"
        }
        result = CourseManager.create(entry)
        self.assertFalse(result)

    def test_create_nonexistent_instructor(self):
        entry = {
            "course_code": "CS103",
            "course_name": "Data Structures",
            "instructor_name": "nonexistent_instructor"
        }
        result = CourseManager.create(entry)
        self.assertFalse(result)

    def test_create_missing_fields(self):
        entry = {
            "course_code": "CS104"
        }
        result = CourseManager.create(entry)
        self.assertFalse(result)


    #view() Tests
    def test_view_valid_course(self):
        result = CourseManager.view(self.course.course_id)
        self.assertIsNotNone(result)
        self.assertEqual(result["course_code"], "CS101")

    def test_view_invalid_course(self):
        result = CourseManager.view(999)# invalid ID

        self.assertIsNone(result)
#update() Tests
    def test_update_successful(self):
        entry = {
            "user_names": ["test_instructor"],
            "course_name": "Updated Course Name"
        }
        result = CourseManager.update(self.course.course_id, entry)
        self.assertTrue(result)
        updated_course = Course.objects.get(course_id=self.course.course_id)
        self.assertEqual(updated_course.course_name, "Updated Course Name")

    def test_update_invalid_course(self):
        entry = {
            "user_names": ["test_instructor"],
            "course_name": "Nonexistent Course"
        }
        result = CourseManager.update(999, entry)  # Invalid course ID
        self.assertFalse(result)

    def test_update_nonexistent_instructor(self):
        entry = {
            "user_names": ["nonexistent_instructor"]
        }
        result = CourseManager.update(self.course.course_id, entry)
        self.assertFalse(result)

#delete() Tests
    def test_delete_successful(self):
        result = CourseManager.delete(self.course.course_id)
        self.assertTrue(result)
        self.assertFalse(Course.objects.filter(course_id=self.course.course_id).exists())

    def test_delete_fail(self):
        result = CourseManager.delete(999)  # Invalid course ID
        self.assertFalse(result)
