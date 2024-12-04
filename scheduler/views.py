from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from manager.LoginManager import LoginManager
from django.contrib import messages
from .models import User

class LoginView(View):
    def get(self, request):
        # Render the login page when accessed via GET
        return render(request, "login.html", {})

    def post(self, request):
        def post(self, request):
            # Extract username and password from POST data
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Use the LoginManager to verify credentials
            user = LoginManager.verify_credentials(username, password)

            if user is None:
                # Handle invalid credentials
                messages.error(request, "Invalid username or password.")
                return render(request, "login.html", {"message": "Invalid username or password."})

            # Successful login
            request.session["username"] = user.username  # Save user in session
            login(request, user)  # Use Django's session management

            # Redirect based on user role
            if user.role == "Admin":
                return redirect("/admin_dashboard/")
            elif user.role == "TA":
                return redirect("/ta_dashboard/")
            elif user.role == "Instructor":
                return redirect("/instructor_dashboard/")
            else:
                return redirect("/")  # Default