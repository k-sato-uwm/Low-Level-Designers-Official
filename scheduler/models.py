from django.db import models

class User(models.Model):
    user_id = models.IntegerField # e.g. 991376811, the PAWS ID#- We won't really use this in tha code
    username = models.CharField(max_length=25, unique = True)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=20)
    email = models.CharField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True) # Optional fields, but we don't want them to be null so we use blank
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username

class Course(models.Model):
    course_id = models.IntegerField(unique=True) # eg 11912
    course_name = models.CharField(max_length=50) # eg COMPSCI 361-401
    instructor_id = models.ForeignKey(User, on_delete=models.SET_NULL) # Instructor teaching the course, if instructor is deleted course can still exist w/o assignment

    def __str__(self):
        return self.course_name

class Lab(models.Model):
    section_id = models.IntegerField() # eg 10933
    course = models.ForeignKey(Course, on_delete=models.CASCADE) # Course the lab section is a part of, section is deleted if course is deleted
    section_number = models.IntegerField() # eg 801, 802
    ta = models.ForeignKey(User, on_delete=models.SET_NULL, optional=True) # TA leading the section, if TA is deleted the section still exists

    def __str__(self):
        return f'{self.course.course_name}-{self.section_number}'