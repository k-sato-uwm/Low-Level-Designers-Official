from django.db import models

class User(models.Model):
    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username


class Lab(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='labs')
    section_number = models.CharField(max_length=25)
    ta = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_labs')

    def __str__(self):
        return f"{self.course.course_name} - {self.section_number}"


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')

    def __str__(self):
        return self.course_name