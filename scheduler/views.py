from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import User

class Create(View):
    def get(self, request):
        # Retrieve the user ID from query parameters (?id=1)
        user_id = request.GET.get('id')

        if user_id:
            # Fetch the user object or return 404 if not found
            user = get_object_or_404(User, id=user_id)
            return render(request, 'user_management.html', {'user': user})

        # If no user ID provided, render the template with an error message
        return render(request, 'user_management.html')

    def post(self, request):
        action = request.POST.get('action')

        if action == 'add':
            role = request.POST.get('role')
            username = request.POST.get('username')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number', '')
            lab_section = request.POST.get('lab_section', '')
            course_section = request.POST.get('course_section', '')
            course = request.POST.get('course', '')

            # Create a new user based on role
            User.objects.create(
                username=username,
                email=email,
                phone_number=phone_number,
                role=role
            )
            return render(request, 'user_management.html', {
                'success': f'{role} {username} added successfully!'
            })

        elif action == 'delete':
            # Handle deletion logic (already implemented in your earlier logic)
            role = request.POST.get('role')
            user_id = request.POST.get('id')
            user = get_object_or_404(User, id=user_id)
            user.delete()
            return render(request, 'user_management.html', {
                'success': f'{role} deleted successfully!'
            })

        elif action == 'edit':
            # Handle edit logic (already implemented in your earlier logic)
            user_id = request.POST.get('id')
            user = get_object_or_404(User, id=user_id)
            user.username = request.POST.get('username', user.username)
            user.email = request.POST.get('email', user.email)
            user.phone_number = request.POST.get('phone_number', user.phone_number)
            user.address = request.POST.get('address', user.address)
            user.role = request.POST.get('role', user.role)
            user.save()
            return render(request, 'user_management.html', {
                'success': f'{user.role} {user.username} updated successfully!'
            })

        return render(request, 'user_management.html', {
            'error': 'Invalid action'
        })