from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from ManagerClasses.CourseManager import CourseManager
from scheduler.models import User, Course


class CourseManagement(View):
    template_name = 'CourseManagement.html'

    def get(self, request):
        # get all courses and instructors
        courses = Course.objects.all().only('course_code', 'course_name', 'instructor_id')
        instructors = User.objects.filter(role='Instructor').only('username', 'user_id')

        context = {
            'courses': courses,
            'instructors': instructors
        }

        return render(request, self.template_name, context)

    def post(self, request):
        # add course
        if 'add_course' in request.POST:
            entry = {
                'course_code': request.POST.get('course_code'),
                'course_name': request.POST.get('course_name'),
                'instructor_name': request.POST.get('instructor_name')
            }

            if not all(entry.values()):  # Check for missing values
                messages.error(request, "All fields are required to add a course.")
                return redirect('course_management')

            success = CourseManager.create(entry)
            if success:
                messages.success(request, "Course added successfully.")
            else:
                messages.error(request, "Failed to add course. It may already exist, or the instructor was not found.")
            return redirect('course_management')

        # delete course
        if 'delete_course' in request.POST:
            course_id = request.POST.get('course_id')
            if not course_id:
                messages.error(request, "Course ID is required to delete.")
                return redirect('course_management')

            success = CourseManager.delete(course_id)
            if success:
                messages.success(request, "Course deleted successfully.")
            else:
                messages.error(request, "Failed to delete course. Course may not exist.")
            return redirect('course_management')

        # edit course
        if 'edit_course' in request.POST:
            course_id = request.POST.get('course_id')
            instructor_name = request.POST.get('instructor_name')

            if not course_id or not instructor_name:
                messages.error(request, "Course ID and Instructor name are required to update.")
                return redirect('course_management')

            entry = {'instructor_name': instructor_name}
            success = CourseManager.update(course_id, entry)
            if success:
                messages.success(request, "Course updated successfully.")
            else:
                messages.error(request, "Failed to update course. Instructor or course may not exist.")
            return redirect('course_management')

        # Default redirect for unrecognized POST actions
        messages.error(request, "Invalid action.")
        return redirect('course_management')
