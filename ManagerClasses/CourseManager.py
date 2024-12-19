from scheduler.models import *
from ManagerABC import AbstractManager
class CourseManager(AbstractManager):
    @staticmethod
    def create(entry: dict) -> bool:
        '''
        :param entry:
            Contains string course_code, string course_name, and optional string instructor_name
        :return:
            True if successful, False if not
        '''
        if Course.objects.filter(course_code=entry.get('course_code')).exists():
            print("Course with the given course_code already exists.")
            return False
        try:
            newcourse = Course.objects.create(
                course_code=entry.get('course_code'),
                course_name=entry.get('course_name'),
            )

            if entry.get('instructor_name'):
                instructor = User.objects.get(username=entry.get('instructor_name'))
                Assignments.objects.create(
                    user = instructor,
                    course = newcourse
                )

            return True
        except User.DoesNotExist:
            print("Instructor does not exist.")
            return False
        except KeyError as e:
            print(f"Missing required field: {e}")
            return False
        except Exception as e:
            print(f'Error creating new course: {e}')
            return False

    @staticmethod
    def view(course_id: int) -> dict | None:
        try:
            course = Course.objects.get(course_id=course_id)
            assignments = course.assignments.all()

            res = {
                    "course_id": course.course_id,
                    "course_code": course.course_code,
                    "course_name": course.course_name,
                    "users": []
                }
            for assignment in assignments:
                res['users'].append(assignment.user)

            return res
        except Course.DoesNotExist:
            print(f"Course with ID {course_id} does not exist.")
            return None

    @staticmethod
    def update(course_id: int, entry: dict) -> bool:
        '''
        :param course_id: int of the ID# of the course you want to edit
        :param entry: 'course_name' : New name of the course (string), 'user_names' : list of usernames of users newly
        assigned to course (string list)
        :return:
        True if successful, False if not
        '''
        try:
            course = Course.objects.get(course_id=course_id)
            if "user_names" in entry:
                for user in entry['user_names']:
                    instructor = User.objects.get(username=user)
                    if not Assignments.objects.filter(course=course,user=instructor).exists():
                        Assignments.objects.create(course=course, user=instructor)
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
        except Exception as e:
            print(f'Error updating course: {e}')
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