from email.policy import default
from django.shortcuts import render

from .models import Student
from .models import Teacher

from .forms import StudentForm
from .forms import TeacherForm

def index(request):
    teachers = Teacher.objects.all()
    return render(request, 'Content/index.html', {'teachers': teachers})

def teacherForm(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)

        if form.is_valid():
            nameInput = request.POST.get('name', None)
            emailInput = request.POST.get('email', None)
            departmentInput = request.POST.get('department', None)
            subjectsInput = request.POST.getlist('subjects', None)

            Teacher.objects.update_or_create(department=departmentInput, email=emailInput, defaults = {"name" : nameInput})
            Teacher.areas.add(subjectsInput)

    else:
        form = TeacherForm()

    return render(request, "Content/teacherForm.html", {'form': form})

def studentForm(request):
    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            nameInput = request.POST.get('Name', None)
            emailInput = request.POST.get('Email', None)
            dobInput = request.POST.get('DOB', None)
            subjectInput = request.POST.get('Subjects', None)

            Student.objects.update_or_create(Email=emailInput, defaults = {"Name" : nameInput, "DOB": dobInput, "Subjects" : subjectInput}) 

    else:
        form = StudentForm()

    return render(request, "Content/studentForm.html", {'form': form})