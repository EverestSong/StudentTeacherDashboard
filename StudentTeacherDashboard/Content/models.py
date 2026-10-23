from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator

class Subject(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    roleChoices = [
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    ]
    
    role = models.CharField(max_length=25, choices=roleChoices)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.CharField(max_length=40)
    subjects = models.ManyToManyField(Subject, blank=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField(validators=[MinValueValidator(date(2000, 1, 1)), MaxValueValidator(date(2026, 1, 1))])
    year_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    subjects = models.ManyToManyField(Subject, blank=True) 

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Unit(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True)
    course_code = models.CharField(max_length=10)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    #unit_outline
    #unit_planner

    def __str__(self):
        return self.name

class UnitOutline(models.Model):
    # Choices
    semesterChoices = [('S1', 'S1'), ('S2', 'S2')]
    accreditationChoices = [('T', 'T'), ('A', 'A'), ('M', 'M')]

    # Fields
    year = models.PositiveIntegerField()
    semester = models.CharField(max_length=2, choices=semesterChoices, default='S1')
    course = models.ForeignKey(Subject, on_delete=models.CASCADE)
    unit = models.OneToOneField(Unit, on_delete=models.CASCADE)
    accreditation = models.CharField(max_length=1, choices=accreditationChoices)
    year_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    unit_goals = models.TextField()
    content_descriptions = models.TextField()

    @property
    def assessment_period(self):
        return f"{self.year} {self.semester}"

    def __str__(self):
        return self.unit.name

class Assessment(models.Model):
    assessmentTypes = [('Test', 'Test'), ('Assignment', 'Assignment'), ('Design', 'Design'), ('Project', 'Project'), 
                       ('Laboratory Task', 'Laboratory Task'), ('Essay', 'Essay'), ('Presentation', 'Presentation')]

    outline = models.ForeignKey(UnitOutline, on_delete=models.CASCADE, related_name='assessments')
    name = models.CharField(max_length=100)
    assessment_type = models.CharField(max_length=20, choices=assessmentTypes)
    weighting = models.DecimalField(max_digits=5, decimal_places=2)
    due_date = models.DateField()

    def __str__(self):
        return self.name
