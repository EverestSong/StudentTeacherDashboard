from django.db import models
from django.utils import timezone

class Subject(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100, unique=True)
    areas = models.ManyToManyField(Subject, blank=True) 

class Student(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100, unique=True)
    date_of_birth = models.DateField(default=timezone.now)
    subjects = models.ManyToManyField(Subject, blank=True) 