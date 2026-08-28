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
from reportlab.platypus import Table, TableStyle, Paragraph
from django.http import FileResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from reportlab.lib import colors
from io import BytesIO
from django.shortcuts import get_object_or_404
from reportlab.lib.styles import getSampleStyleSheet

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

def report(request, outline_id):
    outline = get_object_or_404(UnitOutline, pk=outline_id)
    response = FileResponse(generate_pdf(outline), as_attachment=True, filename=f"{outline.unit} Unit Outline.pdf")
    return response

def generate_pdf(outline):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    # Images and Text
    p.drawImage("dc.png", 30, 720, width=150, height=80)

    p.setFont("Helvetica", 24)
    p.drawString(260, 750, "Dickson College")

    # Unit Data
    outlineLines = [
        ("Assessment Period:", outline.assessment_period),
        ("Course:", outline.course),
        ("Unit:", outline.unit),
        ("Accreditation:", outline.accreditation),
        ("Year Level:", outline.year_level),
    ]

    # Table
    table = Table(outlineLines, colWidths=[120, 380])

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor('#a8c5ff')),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold")]))

    table.wrapOn(p, 500, 700)
    table.drawOn(p, 30, 610)

    # Unit Image
    p.setFont("Helvetica", 14)
    p.drawString(30, 590, "Unit Image")
    p.drawImage(outline.unit.image.path, 30, 500, width=150, height=80)

    # Unit Goals
    styles = getSampleStyleSheet()
    bodyStyle = styles["BodyText"]

    p.drawString(30, 460, "Unit Goals")
    goalsText = Paragraph(outline.unit_goals.replace("\n", "<br/>"), bodyStyle)
    goals_width, goals_height = goalsText.wrap(500, 400)
    goalsText.drawOn(p, 30, 450 - goals_height)

    # Content Descriptions
    p.drawString(30, 360, "Content Descriptions")
    content_text = Paragraph(outline.content_descriptions.replace("\n", "<br/>"), bodyStyle)
    content_width, content_height = content_text.wrap(500, 350)
    content_text.drawOn(p, 30, 350 - content_height)

    # Finish
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer

def edit_outline(request, outline_id):
    outline = get_object_or_404(UnitOutline, pk=outline_id)

    if request.method == "POST":
        form = UnitOutlineForm(request.POST, instance=outline)

        if form.is_valid():
            form.save()
            return redirect("index")

    else:
        form = UnitOutlineForm(instance=outline)

    return render(request, "Content/unitOutlineForm.html", {'form': form})

def delete_outline(request, outline_id):
    outline = get_object_or_404(UnitOutline, pk=outline_id)
    outline.delete()
    return redirect("index")

    
