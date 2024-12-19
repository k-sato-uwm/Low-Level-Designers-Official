from django.shortcuts import render, redirect
from django.views import View
from ManagerClasses.CourseManager import CourseManager
from ManagerClasses.LoginManager import LoginManager
from scheduler.models import User, Course
from ManagerClasses.userManager import UserManagement
from django.contrib import messages


class CourseManagement(View):
    template_name = 'CourseManagement.html'

    def get(self, request):
        # get all courses and instructors
        ids = Course.objects.values('course_id')
        courses = []

        for entry in ids: # Getting all the courses
            courses.append(CourseManager.view(entry['course_id']))

        for course in courses: # Isolating the instructor (first instructor found is listed as "main" instructor
            users = course['users']
            for user in users:
                if user.role == 'Instructor':
                    course['instructor'] = user
                    break

        users = User.objects.values()

        context = {
            'courses': courses,
            'users': users
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
            user_names = request.POST.getlist('user_names')

            if not course_id or not user_names:
                messages.error(request, "Course ID and Instructor name are required to update.")
                return redirect('course_management')

            entry = {'user_names': user_names}
            success = CourseManager.update(course_id, entry)
            if success:
                messages.success(request, "Course updated successfully.")
            else:
                messages.error(request, "Failed to update course. Instructor or course may not exist.")
            return redirect('course_management')

        # Default redirect for unrecognized POST actions
        messages.error(request, "Invalid action.")
        return redirect('course_management')

class LoginView(View):
    def get(self, request):
        # Render the login page when accessed via GET
        return render(request, "login.html", {})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Call LoginManager to verify credentials
        result = LoginManager.verify_credentials(username, password)

        if not result["success"]:
            # If unsuccessful, show an error message
            messages.error(request, result["message"])
            return render(request, "login.html", {"message": result["message"]})

        # On success, simulate login using session or return success message
        user = result['user']
        # login(request, user)
        request.session["username"] = user.username
        request.session['role'] = user.role

        # Redirect based on user role
        # if user.role == "Admin":
        #     return redirect("/admin_dashboard/")
        # elif user.role == "TA":
        #     return redirect("/ta_dashboard/")
        # elif user.role == "Instructor":
        #     return redirect("/instructor_dashboard/")
        # else:
        #     return redirect("/")  # Default
        return redirect("/dashboard/")

class Dashboard(View):
    def get(self, request):
        try:
            userrole = request.session['role']
            username = request.session['username']
        except Exception as E: # Session not initialized/user not signed in
            return redirect('/')
        match userrole:
            case 'Supervisor':
                return render(request, "SupervisorDash.html", {"name": username})
            case 'Instructor':
                return render(request, "InstDash.html", {"name": username})
            case 'Teaching Assistant':
                return render(request, "TADash.html", {"name": username})

    def post(self, request): #Should not receive POST requests on dashboard page
        raise NotImplementedError('POST Requests should not be received by dashboard page')
        # userrole = request.session['role']
        #
        # match userrole:
        #     case 'Supervisor':
        #         return render(request, "SupervisorDash.html", {"name": request.session['username']})
        #     case 'Instructor':
        #         return render(request, "InstDash.html", {"name": request.session['username']})
        #     case 'Teaching Assistant':
        #         return render(request, "TADash.html", {"name": request.session['username']})

class UserManagementView(View):

    def get(self, request):
        users = User.objects.all()
        return render(request, 'user_management.html', {'users': users})


    def post(self, request):
        instructors = User.objects.filter(role='Instructor')
        supervisors = User.objects.filter(role='Supervisor')
        tas = User.objects.filter(role='TA')

        action = request.POST.get('action')
        # creates an instance of userManagement and assigns it to user_manager
        user_manager = UserManagement()

        if action == 'add':

            # assigns result to the result of the create() method,
            # request.POST gets information from post and passes as param
            #result will be true or false if user was created and saved
            result = user_manager.create(request.POST)



        elif action == 'delete':

            #tries to get id to make sure user exist
            user_id = request.POST.get('id')
            if not user_id:
                result = {'success' : False, 'message' : 'User does not exist'}
            else:
                #assigns result to logic in delete() from helper class
                #result will true or false whether user was deleted
                result = user_manager.delete(user_id)


        elif action == 'edit':

            # checks for id to see if user exist
            user_id = request.POST.get('id')
            if not user_id:
                result = {'success': False, 'message': 'User ID is required for editing.'}
            else:

                # assigns result to the logic from the update() from helper class
                #will return true or false whether user was updated
                result = user_manager.update(user_id, request.POST)

        else:
            result = {'success': False, 'message': 'Invalid action specified.'}

        if result['success']:
            messages.success(request, result['message'])
        else:
            messages.error(request, result['message'])

        # this renders the result
        # if result['success'] is true then the success message will display, else it will do nothing
        # if result['success'] is false then the error message will display, else it will do nothing

        users = User.objects.all()
        return render(request, 'user_management.html', {
            'users': users,
            'success': result['message'] if result ['success'] else None,
            'error': result['message'] if not result ['success'] else None,
        })
class CourseEditView(View):
    pass
