from django.db import models

# Custom User Model
class User(models.Model):
    INSTRUCTOR = 'Instructor'
    TEACHING_ASSISTANT = 'Teaching Assistant'
    SUPERVISOR = 'Supervisor'

    ROLE_CHOICES = [
        (INSTRUCTOR, 'Instructor'),
        (TEACHING_ASSISTANT, 'Teaching Assistant'),
        (SUPERVISOR, 'Supervisor'),
    ]
    user_id = models.AutoField(primary_key=True) #Unigue id, for now just pk
    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)# Instructor or Teaching Assistant or Supervisor
    email = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

# Lab Model
class Lab(models.Model):
    lab_id = models.AutoField(primary_key=True) #Unigue id, for now just pk
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='labs')
    section_number = models.CharField(max_length=25) #EX 808,801
    # ta = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='labs_as_ta')

    def __str__(self):
        return f'Lab {self.section_number}'

# Course Model
class Course(models.Model):
    course_id = models.AutoField(primary_key=True) #Unigue id, for now just pk
    course_code = models.CharField(max_length=20, unique=True) #Ex CS101
    course_name = models.CharField(max_length=50) #Ex. Intro to SE
    # instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_as_instructor')

    def __str__(self):
        return self.course_name

# Assignment Table
class Assignments(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments') # User and course are required
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments', null=True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, related_name='assignments', null=True, default = '') # Lab can be null (eg user is assigned to course and not a lab)