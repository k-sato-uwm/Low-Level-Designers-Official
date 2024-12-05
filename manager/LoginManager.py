from django.contrib.auth import login, logout
from django.contrib import messages
from scheduler.models import User
class LoginManager:
    @staticmethod
    def verify_credentials(username, password):
        try:
            # Check if the user exists
            user = User.objects.get(username=username, password=password)
            if user.password==password:  # Validate password
                return {"success": True, "user": user}
            else:
                return {"success": False, "message": "Incorrect password."}
        except User.DoesNotExist:
            return {"success": False, "message": "User not found."}

    def logout_user(request):
        logout(request)
    def is_user_logged_in(request):
        return request.user.is_authenticated

