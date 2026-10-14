from django import forms
from .models import Student, Teacher, Unit, UnitOutline, Assessment
from django.db import models
from datetime import datetime
from django.forms import inlineformset_factory

class TeacherForm(forms.ModelForm):
    class Meta: 
        model = Teacher
        fields = ['department', 'subjects']

        widgets = {
            'department': forms.TextInput(attrs={'placeholder': 'e.g. Mathematics'}),
            'subjects': forms.CheckboxSelectMultiple()
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['date_of_birth', 'year_level', 'subjects']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
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
    currentYear = datetime.today().year
    yearChoices = []
    for year in range(currentYear-2, currentYear+3): # 2024, 2025, 2026, 2027, 2028
        yearChoices.append((year, str(year)))

    year = forms.ChoiceField(choices=yearChoices, initial=datetime.now().year)

    class Meta:
        model = UnitOutline
        fields = ['year', 'semester', 'course', 'unit', 'accreditation', 'year_level', 'unit_goals', 'content_descriptions']

        widgets = {
            'unit_goals': forms.Textarea(attrs={'rows': 10, 'cols': 110}),
            'content_descriptions': forms.Textarea(attrs={'rows': 10, 'cols': 110}),
        }

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['name', 'assessment_type', 'weighting', 'due_date']

        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

AssessmentFormSet = inlineformset_factory(UnitOutline, Assessment, form=AssessmentForm, extra=4, can_delete=True)