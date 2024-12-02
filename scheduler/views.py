from django.shortcuts import render
from django.contrib.messages import success
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from manager.userManager import UserManagement
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User



class LoginView(View):
    def get(self, request):
        # Render the login page when accessed via GET
        return render(request, "login.html", {})

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
            login(request, user)  # Django's session management

            # Redirect based on user role
            if user.role == "Admin":
                return redirect("/admin_dashboard/")
            elif user.role == "TA":
                return redirect("/ta_dashboard/")
            elif user.role == "Instructor":
                return redirect("/instructor_dashboard/")
            else:
                return redirect("/")  # Default fallback

class Dashboard(View):
    def get(self, request):
        userrole = request.session['user']['role']

        match userrole:
            case 'Supervisor':
                return render(request, "SupervisorDash.html", {"name": request.session['user']['username']})
            case 'Instructor':
                return render(request, "InstDash.html", {"name": request.session['user']['username']})
            case 'Teaching Assistant':
                return render(request, "TADash.html", {"name": request.session['user']['username']})

    def post(self, request): #Should not receive POST requests on dashboard page
        userrole = request.session['user']['role']

        match userrole:
            case 'Supervisor':
                return render(request, "SupervisorDash.html", {"name": request.session['user']['username']})
            case 'Instructor':
                return render(request, "InstDash.html", {"name": request.session['user']['username']})
            case 'Teaching Assistant':
                return render(request, "TADash.html", {"name": request.session['user']['username']})

class UserManagementView(View):
    def get(self, request):
        return render(request, 'user_management.html')


    def post(self, request):

        #action to keep track if user clicks add, edit, or delete
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
                result = user_manager.delete(request.POST.get('id'))


        elif action == 'edit':

            # checks for id to see if user exist
            user_id = request.POST.get('id')
            if not user_id:
                result = {'success': False, 'message': 'User ID is required for editing.'}
            else:

                # assigns result to the logic from the update() from helper class
                #will return true or false whether user was updated
                result = user_manager.update(user_id)

        else:
            result = {'success': False, 'message': 'Invalid action specified.'}

        # this renders the result
        # if result['success'] is true then the success message will display, else it will do nothing
        # if result['success'] is false then the error message will display, else it will do nothing
        return render(request, 'user_management.html', {
            'success': result['message'] if result['success'] else None,
            'error': result['message'] if not result['success'] else None,
        })