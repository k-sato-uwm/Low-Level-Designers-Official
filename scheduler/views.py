from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from ManagerClasses.CourseManager import CourseManager
from scheduler.models import User, Course
from manager.userManager import UserManagement
from django.contrib.auth import login

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

class LoginView(View):
    def get(self, request):
        # Render the login page when accessed via GET
        return render(request, "login.html", {"message" : "welcome"})

    def post(self, request):
        # Extract username and password from POST data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Initialize flags for specific errors
        no_such_user = False
        bad_password = False
        user = None  # Initialize the 'user' variable to avoid warnings.

        try:
            # Try to retrieve the user from the database
            user = User.objects.get(username=username)
            bad_password = (user.password != password)  # Check if the password matches
        except User.DoesNotExist:
            no_such_user = True

        if no_such_user:
            # Handle case where user does not exist (optional: auto-register the user)
            messages.error(request, "User does not exist. Please register.")
            return render(request, "login.html", {"message": "User does not exist."})

        elif bad_password:
            # Handle case where the password is incorrect
            return render(request, "login.html", {"message": "Incorrect password."})

        else:
            # Successful login
            request.session["username"] = user.username  # Save user in session
            request.session['role'] = user.role
            login(request, user)  # Django's session management

            return redirect("dashboard/")
            # else:
            #     return redirect("/")  # Default fallback

class Dashboard(View):
    def get(self, request):
        userrole = request.session['role']
        username

        match userrole:
            case 'Supervisor':
                return render(request, "SupervisorDash.html", {"name": request.session['username']})
            case 'Instructor':
                return render(request, "InstDash.html", {"name": request.session['username']})
            case 'Teaching Assistant':
                return render(request, "TADash.html", {"name": request.session['username']})

    def post(self, request): #Should not receive POST requests on dashboard page
        pass
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
    # creates an instance of userManagement and assigns it to user_manager
    user_manager = UserManagement()

    def get(self, request):
        return render(request, 'user_management.html')

    def post(self, request):

        #action to keep track if user clicks add, edit, or delete
        action = request.POST.get('action')

        if action == 'add':

            # assigns result to the result of the create() method,
            # request.POST gets information from post and passes as param
            #result will be true or false if user was created and saved
            result = self.user_manager.create(request.POST)


        elif action == 'delete':

            #tries to get id to make sure user exist
            user_id = request.POST.get('id')
            if not user_id:
                result = {'success' : False, 'message' : 'User does not exist'}
            else:
                #assigns result to logic in delete() from helper class
                #result will true or false whether user was deleted
                result = self.user_manager.delete(request.POST.get('id'))


        elif action == 'edit':

            # checks for id to see if user exist
            user_id = request.POST.get('id')
            if not user_id:
                result = {'success': False, 'message': 'User ID is required for editing.'}
            else:

                # assigns result to the logic from the update() from helper class
                #will return true or false whether user was updated
                result = self.user_manager.update(user_id)

        else:
            result = {'success': False, 'message': 'Invalid action specified.'}

        # this renders the result
        # if result['success'] is true then the success message will display, else it will do nothing
        # if result['success'] is false then the error message will display, else it will do nothing
        return render(request, 'user_management.html', {
            'success': result['message'] if result['success'] else None,
            'error': result['message'] if not result['success'] else None,
        })
