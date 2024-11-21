from django.db import models

class User(models.Model):
    primary_key = models.IntegerField(primary_key=True)
    user_id = models.IntegerField
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=20)
    email = models.CharField()
    phone_number = models.CharField()
    address = models.CharField()

class Lab(models.Model):
    primary_key = models.IntegerField(primary_key=True)
    course_id = models.IntegerField()
    section_number = models.CharField(max_length=25)
    ta_id = models.IntegerField()

class Course(models.Model):
    primary_key = models.IntegerField(primary_key=True)
    course_id = models.IntegerField()
    course_name = models.CharField(max_length=50)
    lab_section = models.ForeignKey(Lab, on_delete=models.CASCADE)
    instructor_id = models.ForeignKey(User, on_delete=models.CASCADE)