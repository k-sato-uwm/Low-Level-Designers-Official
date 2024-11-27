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
