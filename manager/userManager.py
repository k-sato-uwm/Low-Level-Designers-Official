class UserManagement:

    def create(self, entry):
        # everything below in comments is basically the code for the create method
        # try: // gets info
        #  role = request.POST.get('role')
        #  username = request.POST.get('username')
        # email = request.POST.get('email')
        # phone_number = request.POST.get('phone_number', '')
        # address = request.POST.get('address', '')
        # password = request.POST.get('password', '')


        # user = User(  //creating a new user
        #     role=role,
        #     username=username,
        #    email=email,
        #     phone_number=phone_number,
        #    address=address,
        #  password=password
        #   )
        # user.save()
        #// the code right below this returns a true or false along with a message or throws an exception
        #  return {'success': True, 'message': f'{role} {username} added successfully!'}
        #         except IntegrityError:
        #             return {'success': False, 'message': 'User already exists!'}
        # everything in comments above is basically the code for the create method
        pass

    def view(self, user_id):
        pass

    def update(self, user):
        pass

    def delete(self, user_id):
        pass