from django.shortcuts import render, redirect
from datetime import datetime
from django.shortcuts import get_object_or_404

# User authentication
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Models and associated forms
from .models import Student, Teacher, Unit, UnitOutline, Assessment
from .forms import StudentForm, TeacherForm, UnitForm, UnitOutlineForm, AssessmentFormSet, AccountForm

# PDF generation
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, PageBreak, Spacer
from django.http import FileResponse
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def index(request):
    return render(request, 'Content/index.html')

@login_required
def studentDashboard(request):
    units = Unit.objects.all()
    outlines = UnitOutline.objects.all()
    assessments = Assessment.objects.all()

    return render(request, 'Content/studentDashboard.html', {'units': units, 'outlines': outlines, 'assessments': assessments})

@login_required
def teacherDashboard(request):
    if request.user.role != 'Teacher':
        raise PermissionDenied("You must be signed in to a teacher account to use the teacher dashboard.")

    teachers = Teacher.objects.all()
    students = Student.objects.all()
    units = Unit.objects.all()
    outlines = UnitOutline.objects.all()
    assessments = Assessment.objects.all()

    return render(request, 'Content/teacherDashboard.html', {'teachers': teachers, 'students': students, 'units': units, 'outlines': outlines, 'assessments': assessments})

def signIn(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if request.user.role == 'Student':
                return redirect('studentDashboard')
            else:
                return redirect('teacherDashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'Content/signIn.html', {'form': form})

def signOut(request):
    logout(request)
    return redirect('index')

@login_required
def teacherForm(request):
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        teacher_form = TeacherForm(request.POST)

        if account_form.is_valid() and teacher_form.is_valid():
            user = account_form.save(commit=False)
            user.role = 'Teacher'
            user.save()
            
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()

            teacher_form.save_m2m()
            return redirect('index')

    else:
        account_form = AccountForm()
        teacher_form = TeacherForm()

    return render(request, 'Content/teacherForm.html', {'account_form': account_form, 'teacher_form': teacher_form})

def studentForm(request):
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        student_form = StudentForm(request.POST)

        if account_form.is_valid() and student_form.is_valid():
            user = account_form.save(commit=False)
            user.role = 'Student'
            user.save()

            student = student_form.save(commit=False)
            student.user = user
            student.save()

            student_form.save_m2m()
            return redirect('index')

    else:
        account_form = AccountForm()
        student_form = StudentForm()

    return render(request, 'Content/studentForm.html', {'account_form': account_form, 'student_form': student_form})

@login_required
def unitForm(request):
    if request.user.role != 'Teacher':
        raise PermissionDenied("You must be signed in to a teacher account to create unit records.")

    if request.method == 'POST':
        form = UnitForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = UnitForm()

    return render(request, 'Content/unitForm.html', {'form': form})

@login_required
def unitOutlineForm(request):
    if request.user.role != 'Teacher':
        raise PermissionDenied("You must be signed in to a teacher account to create unit outline records.")

    outline = UnitOutline(year=datetime.now().year)

    if request.method == 'POST':
        form = UnitOutlineForm(request.POST, instance=outline)
        assessment_formset = AssessmentFormSet(request.POST, instance=outline)

        if form.is_valid() and assessment_formset.is_valid():
            outline = form.save()
            assessment_formset.instance = outline
            assessment_formset.save()
            return redirect('index')

    else:
        form = UnitOutlineForm(instance=outline)
        assessment_formset = AssessmentFormSet(instance=outline)

    return render(request, 'Content/unitOutlineForm.html', {'form': form, 'assessment_formset': assessment_formset})

@login_required
def report(outline_id):
    outline = get_object_or_404(UnitOutline, pk=outline_id)
    response = FileResponse(generate_pdf(outline), as_attachment=True, filename=f"{outline.unit} Unit Outline {datetime.now().year}.pdf")
    return response

@login_required
def generate_pdf(outline):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40)
    styles = getSampleStyleSheet()
    elements = []

    template = [
        ("GRID", (0, 0), (-1, -1), 1, colors.black), # Black table outline
        ("PADDING", (0, 0), (-1, -1), 5), # 5 pixels of padding
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor('#a8c5ff')), # First column is blue
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold") # First column is Helvetica-Bold
    ]

    # Title
    title = Paragraph("Dickson College", styles["Title"])
    elements.append(title)
    elements.append(Spacer(0, 10))

    # Logo
    logo = Image("dc.png", width=150, height=80, hAlign='LEFT')
    elements.append(logo)
    elements.append(Spacer(0, 10))

    # Unit
    elements.append(Paragraph("Unit", styles["h2"]))
    outlineLines = [
        ("Assessment Period:", outline.assessment_period),
        ("Course:", outline.course),
        ("Unit:", outline.unit),
        ("Accreditation:", outline.accreditation),
        ("Year Level:", outline.year_level),
    ]

    table = Table(outlineLines, colWidths=[120, 380])

    table.setStyle(TableStyle(template)) 

    elements.append(table)
    elements.append(Spacer(0, 10))

    # Unit Image
    elements.append(Paragraph("Unit Image", styles["h2"]))
    unit_image = Image(outline.unit.image.path, width=150, height=80, hAlign='LEFT')
    elements.append(unit_image)
    elements.append(Spacer(0, 10))

    # Unit Goals
    elements.append(Paragraph("Unit Goals", styles["h2"]))
    goals = Paragraph(outline.unit_goals.replace('\n', '<br/>'), styles["BodyText"])
    elements.append(goals)
    elements.append(Spacer(0, 10))

    # Content Descriptions
    elements.append(Paragraph("Content Descriptions", styles["h2"]))
    descriptions = Paragraph(outline.content_descriptions.replace('\n', '<br/>'), styles["BodyText"])
    elements.append(descriptions)
    elements.append(Spacer(0, 10))

    # Assessments
    elements.append(PageBreak())
    elements.append(Paragraph("Assessments", styles["h2"]))

    for assessment in outline.assessments.all():
        assessmentLines = [
            ("Title:", assessment.name),
            ("Assessment Type:", assessment.assessment_type),
            ("Weighting:", f"{assessment.weighting * 100}%"),
            ("Due Date:", assessment.due_date.strftime('%d/%m/%Y')),
        ]

        table = Table(assessmentLines, colWidths=[120, 380])
        table.setStyle(TableStyle(template)) 
        elements.append(table)
        elements.append(Spacer(0, 10))

        # Old
        '''
        elements.append(Paragraph(assessment.name, styles["h4"]))
        elements.append(Paragraph(f"Assessment Type: {assessment.assessment_type}", styles["BodyText"]))
        elements.append(Paragraph(f"Weighting: {assessment.weighting * 100}%", styles["BodyText"]))
        elements.append(Paragraph(f"Due Date: {assessment.due_date.strftime('%d/%m/%Y')}", styles["BodyText"]))
        '''

    doc.build(elements)

    buffer.seek(0)
    return buffer

@login_required
def editOutline(request, outline_id):
    if request.user.role != 'Teacher':
        raise PermissionDenied("You must be signed in to a teacher account to edit unit outline records.")

    outline = get_object_or_404(UnitOutline, pk=outline_id)

    if request.method == 'POST':
        form = UnitOutlineForm(request.POST, instance=outline)
        assessment_formset = AssessmentFormSet(request.POST, instance=outline)

        if form.is_valid() and assessment_formset.is_valid():
            outline = form.save()
            assessment_formset.instance = outline
            assessment_formset.save()
            return redirect('index')

    else:
        form = UnitOutlineForm(instance=outline)
        assessment_formset = AssessmentFormSet(instance=outline)

    return render(request, 'Content/unitOutlineForm.html', {'form': form, 'assessment_formset': assessment_formset})

@login_required
def deleteOutline(request, outline_id):
    if request.user.role != 'Teacher':
        raise PermissionDenied("You must be signed in to a teacher account to delete unit outline records.")

    outline = get_object_or_404(UnitOutline, pk=outline_id)
    outline.delete()
    return redirect('index')

def rubric(request):
    return render(request, 'Content/rubric.html')
