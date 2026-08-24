from email.policy import default
from django.shortcuts import render, redirect

from .models import Student
from .models import Teacher
from .models import Unit
from .models import UnitOutline

from .forms import StudentForm
from .forms import TeacherForm
from .forms import UnitForm
from .forms import UnitOutlineForm

from pypdf import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from django.http import FileResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from reportlab.lib import colors
from io import BytesIO

def index(request):
    teachers = Teacher.objects.all()
    students = Student.objects.all()
    units = Unit.objects.all()
    outlines = UnitOutline.objects.all()

    return render(request, 'Content/index.html', {'teachers': teachers, 'students': students, 'units': units, 'outlines': outlines})

def teacherForm(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("index")

    else:
        form = TeacherForm()

    return render(request, "Content/teacherForm.html", {'form': form})

def studentForm(request):
    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("index")

    else:
        form = StudentForm()

    return render(request, "Content/studentForm.html", {'form': form})

def unitForm(request):
    if request.method == "POST":
        form = UnitForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("index")

    else:
        form = UnitForm()

    return render(request, "Content/unitForm.html", {'form': form})

def unitOutlineForm(request):
    if request.method == "POST":
        form = UnitOutlineForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("index")

    else:
        form = UnitOutlineForm()

    return render(request, "Content/unitOutlineForm.html", {'form': form})

def report(request):
    pdf_file = staticfiles_storage.path("DigitalSolutions.pdf")

    try:
        merger = PdfWriter()

        input1 = PdfReader(generate_pdf())
        input2 = PdfReader(pdf_file, "rb")

        merger.append(input1)
        merger.append(input2)

        buffer = BytesIO()
        merger.write(buffer)
        buffer.seek(0) 

        response = FileResponse(buffer, as_attachment=True, filename="attachment.pdf")

    except FileNotFoundError:
        response = FileResponse(generate_pdf(), as_attachment=True, filename="noAttachment.pdf")

    return response

def generate_pdf():
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    # Teacher Data
    teachers = Teacher.objects.all()
    teacherLines = [("Name: ", "Email: ", "Department: ", "Subjects: ")]

    for teacher in teachers:
        subjects = ", ".join(subject.name for subject in teacher.subjects.all())
        teacherLines.append((teacher.name, teacher.email, teacher.department, subjects))

    teacherTable = Table(teacherLines)

    teacherTable.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor('#a8c5ff')),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")]))

    teacherTable.wrapOn(p, 500, 700)
    teacherTable.drawOn(p, 10, 580)

    p.drawImage("dc.png", 10, 730, width=150, height=100)
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer