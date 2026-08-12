from django import forms

from .models import Student 
from .models import Teacher 
#from .models import Unit 

from django.db import models

class TeacherForm(forms.ModelForm):
    class Meta: 
        model = Teacher
        fields = ['name', 'email', 'areas']

class StudentForm(forms.ModelForm):
    date_of_birth = forms.DateField()

    class Meta:
        model = Student
        fields = ['name', 'email', 'date_of_birth', 'subjects']
