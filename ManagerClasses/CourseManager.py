from scheduler.models import *
from .ManagerABC import AbstractManager
class CourseManager(AbstractManager):
    @staticmethod
    def create(entry):
        print("start")
        if Course.objects.filter(course_code=entry.get('course_code')).exists():
            return False

        try:
            instructor = User.objects.get(username=entry.get('instructor_name'))
            print(instructor)
            Course.objects.create(
                course_code=entry.get('course_code'),
                course_name=entry.get('course_name'),
                instructor_id=instructor.user_id)
            return True
        except (KeyError, User.DoesNotExist):
            return False

    def view(course_id):
        pass

    def update(course_id,entry):
        try:
            course = Course.objects.get(course_id=course_id)
            #change db entry
            course.instructor = User.objects.get(username=entry.get('instructor_name'))
            course.save()
            return True
        except Course.DoesNotExist:
            return False

    @staticmethod
    def delete(course_id):
        try:
            course = Course.objects.get(course_id=course_id)
            course.delete()
            return True
        except Course.DoesNotExist:
            return False
