from django.shortcuts import render
from django.views import View
from manager.userManager import UserManagement
from scheduler.models import User


class UserManagementView(View):

    def get(self, request):
        instructors = User.objects.filter(role='Instructor')
        supervisors = User.objects.filter(role='Supervisor')
        tas = User.objects.filter(role='TA')

        return render(request, 'user_management.html', {
            'instructors': instructors,
            'supervisors': supervisors,
            'tas': tas,
        })


    def post(self, request):

        #action to keep track if user clicks add, edit, or delete
        action = request.POST.get('action')

        # creates an instance of userManagement and assigns it to user_manager
        user_manager = UserManagement()

        role = request.POST.get('role')

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
                result = user_manager.delete(user_id)


        elif action == 'edit':

            # checks for id to see if user exist
            user_id = request.POST.get('id')
            if not user_id:
                result = {'success': False, 'message': 'User ID is required for editing.'}
            else:

                # assigns result to the logic from the update() from helper class
                #will return true or false whether user was updated
                result = user_manager.update(user_id, request.POST)

        else:
            result = {'success': False, 'message': 'Invalid action specified.'}

        # this renders the result
        # if result['success'] is true then the success message will display, else it will do nothing
        # if result['success'] is false then the error message will display, else it will do nothing
        return render(request, 'user_management.html', {
            'success': result['message'] if result['success'] else None,
            'error': result['message'] if not result['success'] else None,
            'role': role,
        })