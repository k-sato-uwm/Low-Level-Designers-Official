from django.contrib.auth import login, logout
from django.contrib import messages
from scheduler.models import User
class LoginManager:
    @staticmethod
    def verify_credentials(self, username, password):
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                return {'success': True, 'message': 'You have successfully logged in.'}
        except User.DoesNotExist:
            return {'success': False, 'message': 'User does not exist'}
        return None
    def logout_user(request):
        logout(request)
    def is_user_logged_in(request):
        return request.user.is_authenticated

