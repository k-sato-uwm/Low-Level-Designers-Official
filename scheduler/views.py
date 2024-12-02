from django.contrib.messages import success
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.views import View



from manager.userManager import UserManagement
class UserManagementView(View):
    def get(self, request):
        # Retrieve the user ID from query parameters (?id=1)
        user_id = request.GET.get('id')
        return render(request, 'user_management.html')


    def post(self, request):
        action = request.POST.get('action')
        user_manager = UserManagement()
        #add part
        if action == 'add':
         # everything below in comments is basically the code for the create method
         #try:
          #  role = request.POST.get('role')
          #  username = request.POST.get('username')
           # email = request.POST.get('email')
           # phone_number = request.POST.get('phone_number', '')
           # address = request.POST.get('address', '')
           # password = request.POST.get('password', '')


            # Create a new user
            #user = User(
           #     role=role,
           #     username=username,
            #    email=email,
           #     phone_number=phone_number,
            #    address=address,
              #  password=password
         #   )
           # user.save()
         #  return {'success': True, 'message': f'{role} {username} added successfully!'}
         #         except IntegrityError:
         #             return {'success': False, 'message': 'User already exists!'}

         # everything in comments above is basically the code for the create method
            result = user_manager.create(request.POST)



        elif action == 'delete':
            # Handle deletion logic (already implemented in your earlier logic)

            user_id = request.POST.get('id')
            if not user_id:
                result = {'success' : False, 'message' : 'User does not exist'}
            else:
                result = user_manager.delete(request.POST.get('id'))


        elif action == 'edit':
            user_id = request.POST.get('id')
            if not user_id:
                result = {'success': False, 'message': 'User ID is required for editing.'}
            else:
                result = user_manager.update(user_id)

        else:
            result = {'success': False, 'message': 'Invalid action specified.'}

        return render(request, 'user_management.html', {
            'success': result['message'] if result['success'] else None,
            'error': result['message'] if not result['success'] else None,
        })