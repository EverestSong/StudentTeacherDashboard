from django import forms

from .models import Student 
from .models import Teacher 
from .models import Unit 
from .models import UnitOutline

from django.db import models

class TeacherForm(forms.ModelForm):
    class Meta: 
        model = Teacher
        fields = ['name', 'email', 'department', 'subjects']

        widgets = {
            'email': forms.EmailInput(attrs={'size': '26'}),     
            'department': forms.TextInput(attrs={'placeholder': 'e.g. Mathematics'}),
            'subjects': forms.CheckboxSelectMultiple()
        }

class StudentForm(forms.ModelForm):
    date_of_birth = forms.DateField()

    class Meta:
        model = Student
        fields = ['name', 'email', 'date_of_birth', 'year_level', 'subjects']

        widgets = {
            'email': forms.EmailInput(attrs={'size': '28'}),     
            'date_of_birth': forms.TextInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'subjects': forms.CheckboxSelectMultiple()
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name', 'image', 'course_code', 'teacher']

        widgets = {
            'name': forms.TextInput(attrs={'size': '30'}),
            'course_code': forms.TextInput(attrs={'size': '10'}),
        }

class UnitOutlineForm(forms.ModelForm):
    class Meta:
        model = UnitOutline
        fields = ['assessment_period', 'course', 'unit', 'accreditation', 'year_level', 'unit_goals', 'content_descriptions']

        widgets = {
            'accreditation': forms.TextInput(attrs={'size': '1'}),     
            'unit_goals': forms.Textarea(attrs={'rows': 10, 'cols': 100}),
            'content_descriptions': forms.Textarea(attrs={'rows': 10, 'cols': 100}),
        }