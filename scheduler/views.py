from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from manager.LoginManager import LoginManager
from django.contrib import messages
from scheduler.models import User

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
        user = User.objects.get(username=username)
        login(request, user)
        request.session["username"] = user.username

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