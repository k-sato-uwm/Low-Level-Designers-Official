from scheduler.models import Lab, User, Assignments
from ManagerClasses.ManagerABC import AbstractManager
class LabManager(AbstractManager):
    def create(self, data, msg=None):
        try:
            if not isinstance(data, dict):
                raise TypeError("Data must be a dictionary")

            # Extract lab details
            lab_id = data.get('lab_id')
            section_number = data.get('section_number')

            if not isinstance(lab_id, int) or not isinstance(section_number, str):
                return False

            # Check for duplicates
            if Lab.objects.filter(lab_id=lab_id).exists():
                return False

            Lab.objects.create(lab_id=lab_id, section_number=section_number)
            if data.get('ta_name'):
                instructor = User.objects.get(username=data.get('instructor_name'))
                Assignments.objects.create(
                    user = instructor,
                    lab = Lab.objects.get(lab_id=lab_id),
                )
            return True
        except Exception:
            return False

    def view(self, lab_id):
        if not isinstance(lab_id, int):
            raise TypeError("Lab ID must be an integer")

        try:
            lab = Lab.objects.get(lab_id=lab_id)
            return {'lab_id': lab.lab_id, 'section_number': lab.section_number}
        except Lab.DoesNotExist:
            return None

    def update(self, lab_id, data):
        if not isinstance(lab_id, int) or not isinstance(data, dict):
            raise TypeError("Invalid input format")

        try:
            lab = Lab.objects.get(lab_id=lab_id)
            for key, value in data.items():
                if hasattr(lab, key) and isinstance(value, str):
                    setattr(lab, key, value)
            lab.save()
            return True
        except Lab.DoesNotExist:
            return False

    def delete(self, lab_id):
        if not isinstance(lab_id, int):
            raise TypeError("Lab ID must be an integer")

        try:
            lab = Lab.objects.get(lab_id=lab_id)
            lab.delete()
            return True
        except Lab.DoesNotExist:
            return False
