from django.db import IntegrityError
from scheduler.models import User


class UserManagement:
    def create(self, entry):
        try:

            if entry is None:
                return {'success': False, 'message': 'Input data is required.'}

            # make sure fields are filled out
            required_fields = ['role', 'username', 'email', 'password']
            for field in required_fields:
                if not entry.get(field):
                    return {'success': False, 'message': f'{field} is required.'}

            role = entry.get('role')
            username = entry.get('username')
            email = entry.get('email')
            phone_number = entry.get('phone_number', '')
            address = entry.get('address', '')
            password = entry.get('password', '')

            #checks if username already exist
            if User.objects.filter(username=username).exists():
                return {'success': False, 'message': 'User already exists!'}

            #checks if password already exist
            if User.objects.filter(password=password).exists():
                return {'success': False, 'message': 'Password already exists.'}

            #checks to make sure role is valid
            if entry.get('role') not in ["Instructor", "Supervisor", "Teaching Assistant"]:
                return {'success': False, 'message': 'Invalid role specified'}

            user = User(
                role=role,
                username=username,
                email=email,
                phone_number=phone_number,
                address=address,
                password=password,
            )
            user.save()
            return {'success': True, 'message': f'{role} {username} added successfully!'}
        except IntegrityError:
            return {'success': False, 'message': 'User already exists!'}
        except Exception as e:
            return {'success': False, 'message': f'Error occurred: {str(e)}'}

    def update(self, user_id, entry):
        try:

            user = User.objects.get(user_id=user_id)

            #checks to make sure username is not modified to existing username
            new_username = entry.get('username')
            if new_username and User.objects.filter(username=new_username).exists():
                return{'success': False, 'message': 'User with that username already exists.'}

            new_password = entry.get('password')
            if new_password and User.objects.filter(password=new_password).exists():
                return{'success': False, 'message': 'Password already exists.'}

            user.username = entry.get('username', user.username) or user.username
            user.role = entry.get('role', user.role) or user.role
            user.email = entry.get('email', user.email) or user.email
            user.phone_number = entry.get('phone_number', user.phone_number) or user.phone_number
            user.address = entry.get('address', user.address) or user.address
            user.password = entry.get('password', user.password) or user.password

            user.save()
            return {'success': True, 'message': 'User updated successfully!'}
        except User.DoesNotExist:
            return {'success': False, 'message': 'User does not exist!'}
        except Exception as e:
            return {'success': False, 'message': f'Error occurred: {str(e)}'}

    def delete(self, user_id):
        try:

            user = User.objects.get(user_id=user_id)
            user.delete()
            return {'success': True, 'message': 'User deleted successfully!'}
        except User.DoesNotExist:
            return {'success': False, 'message': 'User does not exist!'}
        except Exception as e:
            return {'success': False, 'message': f'Error occurred: {str(e)}'}