from django.db import IntegrityError

from scheduler.models import User


class UserManagement:
    def create(self, entry):
        try:
            role = entry.get('role')
            username = entry.get('username')
            email = entry.get('email')
            phone_number = entry.get('phone_number', '')
            address = entry.get('address', '')
            password = entry.get('password', '')

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

            user = User.objects.get(user_id =user_id)

            user.username = entry.get('username', user.username)
            user.role = entry.get('role', user.role)
            user.email = entry.get('email', user.email)
            user.phone_number = entry.get('phone_number', user.phone_number)
            user.address = entry.get('address', user.address)
            user.password = entry.get('password', user.password)

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