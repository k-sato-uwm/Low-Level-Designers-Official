from django.contrib.auth import logout
from scheduler.models import User
class LoginManager:
    @staticmethod
    def verify_credentials(username, password):
        try:
            # Check if the user exists
            user = User.objects.get(username=username)
            if user.password==password:  # Validate password
                return {"success": True, "user": user}
            else:
                return {"success": False, "message": "Incorrect password."}
        except User.DoesNotExist:
            return {"success": False, "message": "User not found."}

    def logout_user(request):
        pass

    def is_user_logged_in(request):
        pass