from django.test import TestCase
from django.urls import reverse
from scheduler.models import Course, Lab, User, Assignments

class CourseEditViewTest(TestCase):
    def setUp(self):
        # Create users
        self.instructor = User.objects.create(username="instructor1", role=User.INSTRUCTOR)
        self.ta = User.objects.create(username="ta1", role=User.TEACHING_ASSISTANT)

        # Create course
        self.course = Course.objects.create(course_code="CS101", course_name="Intro to Computer Science")

        # Create lab
        self.lab = Lab.objects.create(course=self.course, section_number="Lab 1")

        # Assign TA to the lab
        Assignments.objects.create(user=self.ta, course=self.course, lab=self.lab)

        # URL for editing the course
        self.url = reverse("edit_course", args=[self.course.pk])

    def test_get_course_edit_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_course.html")
        self.assertContains(response, self.course.course_code)
        self.assertContains(response, self.course.course_name)
        self.assertContains(response, self.lab.section_number)

    def test_save_course_details(self):
        response = self.client.post(self.url, {
            "save_course": "true",
            "course_code": "CS102",
            "course_name": "Advanced CS",
            "instructor_id": self.instructor.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.course.refresh_from_db()
        self.assertEqual(self.course.course_code, "CS102")
        self.assertEqual(self.course.course_name, "Advanced CS")

    def test_add_lab_section(self):
        response = self.client.post(self.url, {
            "add_lab": "true",
            "lab_name": "Lab 2",
            "ta_id": self.ta.pk,
        })
        self.assertEqual(response.status_code, 302)
        labs = Lab.objects.filter(course=self.course)
        self.assertEqual(labs.count(), 2)
        self.assertTrue(Lab.objects.filter(section_number="Lab 2").exists())

        # Check if assignment was created
        assignment = Assignments.objects.filter(course=self.course, lab__section_number="Lab 2").first()
        self.assertIsNotNone(assignment)
        self.assertEqual(assignment.user, self.ta)

    def test_edit_lab_section(self):
        new_ta = User.objects.create(username="ta2", role=User.TEACHING_ASSISTANT)
        response = self.client.post(self.url, {
            "edit_lab": "true",
            "lab_id": self.lab.pk,
            "lab_name": "Updated Lab",
            "ta_id": new_ta.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.section_number, "Updated Lab")

        # Check assignment update
        assignment = Assignments.objects.filter(course=self.course, lab=self.lab).first()
        self.assertEqual(assignment.user, new_ta)

    def test_delete_lab_section(self):
        response = self.client.post(self.url, {
            "delete_lab": self.lab.pk,
        })
        self.assertEqual(response.status_code, 302)

        # Check lab and assignment deletion
        self.assertFalse(Lab.objects.filter(pk=self.lab.pk).exists())
        self.assertFalse(Assignments.objects.filter(course=self.course, lab=self.lab).exists())
