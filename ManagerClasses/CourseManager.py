from scheduler.models import *
from ManagerClasses.ManagerABC import AbstractManager
class CourseManager(AbstractManager):
    @staticmethod
    def create(entry: dict) -> bool:
        if Course.objects.filter(course_code=entry.get('course_code')).exists():
            print("Course with the given course_code already exists.")
            return False
        try:
            instructor = User.objects.get(username=entry.get('instructor_name'))
            Course.objects.create(
                course_code=entry.get('course_code'),
                course_name=entry.get('course_name'),
                instructor_id=instructor.user_id
            )
            return True
        except User.DoesNotExist:
            print("Instructor does not exist.")
            return False
        except KeyError as e:
            print(f"Missing required field: {e}")
            return False


    @staticmethod
    def view(course_id: int) -> dict | None:
        try:
            course = Course.objects.get(course_id=course_id)
            return {
                    "course_id": course.course_id,
                    "course_code": course.course_code,
                    "course_name": course.course_name,
                    "instructor": course.instructor_id,
                }
        except Course.DoesNotExist:
            print(f"Course with ID {course_id} does not exist.")
            return None

    @staticmethod
    def update(course_id: int, entry: dict) -> bool:
        try:
            course = Course.objects.get(course_id=course_id)
            if "instructor_name" in entry:
                instructor = User.objects.get(username=entry.get('instructor_name'))
                course.instructor = instructor
            if "course_name" in entry:
                course.course_name = entry.get('course_name')
            course.save()
            return True
        except Course.DoesNotExist:
            print(f"Course with ID {course_id} does not exist.")
            return False
        except User.DoesNotExist:
            print("Instructor does not exist.")
            return False
        except KeyError as e:
            print(f"Missing required field: {e}")
            return False

    @staticmethod
    def delete(course_id: int) -> bool:
        try:
            course = Course.objects.get(course_id=course_id)
            course.delete()
            print(f"Course with ID {course_id} has been deleted.")
            return True
        except Course.DoesNotExist:
            print(f"Course with ID {course_id} does not exist.")
            return False