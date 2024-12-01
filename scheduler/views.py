from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import User
from management.userManager import UserManagement
class User(View):
    def get(self, request):
        # Retrieve the user ID from query parameters (?id=1)
        user_id = request.GET.get('id')
        return render(request, 'user_management.html')

    def post(self, request):
        action = request.POST.get('action')

        if action == 'add':
         try:
            role = request.POST.get('role')
            username = request.POST.get('username')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number', '')
            address = request.POST.get('address', '')
            password = request.POST.get('password', '')

            # Create a new user
            user = User(username=username, email=email, phone_number=phone_number, address=address, password=password, role=role)
            user.save()

            return render(request, 'user_management.html', {
                'success': f'{role} {username} added successfully!'
            })
         except IntegrityError:
             return render(request, 'user_management.html', {'success': ' User already exist!'})



        elif action == 'delete':
            # Handle deletion logic (already implemented in your earlier logic)
         try:
            user_id = request.POST.get('id')
            return render(request, 'user_management.html', {
                'success': ' deleted successfully!'
            })
         except User.DoesNotExist:
             return render(request, 'user_management.html', {'success': 'Error: user not found'})





        elif action == 'edit':
         try:
            user_id = request.POST.get('id')

            return render(request, 'user_management.html', {
                'success': 'updated successfully!'
            })
         except User.DoesNotExist:
             return render(request, 'user_management.html', {'success': 'User not found'})


        return render(request, 'user_management.html', {
            'error': 'Invalid action'
        })