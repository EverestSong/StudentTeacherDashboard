from email.policy import default
from django.shortcuts import render

from .models import Student
from .models import Teacher
from .models import Unit

from .forms import StudentForm
from .forms import TeacherForm
from .forms import UnitForm

def index(request):
    teachers = Teacher.objects.all()
    students = Student.objects.all()
    units = Unit.objects.all()
    return render(request, 'Content/index.html', {'teachers': teachers, 'students': students, 'units': units})

def teacherForm(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)

        if form.is_valid():
            nameInput = request.POST.get('name', None)
            emailInput = request.POST.get('email', None)
            departmentInput = request.POST.get('department', None)
            subjectsInput = request.POST.getlist('subjects', None)

            teacher, created = Teacher.objects.update_or_create(email=emailInput, defaults = {"department": departmentInput, "name" : nameInput})
            teacher.subjects.set(subjectsInput)

    else:
        form = TeacherForm()

    return render(request, "Content/teacherForm.html", {'form': form})

def studentForm(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            nameInput = request.POST.get('name', None)
            emailInput = request.POST.get('email', None)
            dateOfBirthInput = request.POST.get('date_of_birth', None)
            yearLevelInput = request.POST.get('year_level', None)
            subjectsInput = request.POST.getlist('subjects', None)

            student, created = Student.objects.update_or_create(email=emailInput, defaults = {"name" : nameInput, "date_of_birth" : dateOfBirthInput, "year_level": yearLevelInput}) 
            student.subjects.set(subjectsInput)

    else:
        form = StudentForm()

    return render(request, "Content/studentForm.html", {'form': form})

def unitForm(request):
    if request.method == "POST":
        form = UnitForm(request.POST, request.FILES)

        if form.is_valid():
            nameInput = request.POST.get('name', None)
            imageInput = request.POST.get('image', None)

            Unit.objects.create(name=nameInput, image=imageInput) 

    else:
        form = UnitForm()

    return render(request, "Content/unitForm.html", {'form': form})