from django.contrib.auth.models import User
from django.db import models
import uuid
import os
# Create your models here.

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('avatars', filename)

class Course(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=30, null=True)
    surname = models.CharField(max_length=30, null=True)
    room = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    description = models.TextField(default="")
    photo = models.FileField(upload_to=get_file_path, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name + " " + self.surname

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(default="")