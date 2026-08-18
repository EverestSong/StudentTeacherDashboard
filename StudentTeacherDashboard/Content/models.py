from django.db import models
from django.utils import timezone
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator

class Subject(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100, unique=True)
    department = models.CharField(max_length=40)
    subjects = models.ManyToManyField(Subject, blank=True) 

class Student(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100, unique=True)
    date_of_birth = models.DateField(default=timezone.now, validators=[MinValueValidator(date(2000, 1, 1)), MaxValueValidator(date(2026, 1, 1))])
    year_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    subjects = models.ManyToManyField(Subject, blank=True) 

class Unit(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True)
    #course_code = models.CharField(max_length=10)
    #teacher = models.CharField(max_length=25)
    #unit_outline
    #unit_planner

    def __str__(self):
        return self.name