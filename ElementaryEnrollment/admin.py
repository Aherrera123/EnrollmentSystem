from django.contrib import admin
from django import forms
from ElementaryEnrollment.models import Student, Enrollment, Mother, Father, Document, ArchivedAccount, Schedule, Section, Subject, EnrollmentPeriod, TimeSlot
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from django.db.models import Count
from django.conf import settings
import os

# Register your models here. 





class RegistrarAdminMixin:
    def has_module_permission(self, request):
        if request.user.groups.filter(name='Registrar').exists():
            return True
        return super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        if request.user.groups.filter(name='Registrar').exists():
            return True
        return super().has_view_permission(request, obj)
    def generate_cor(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="certificate_of_registration.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        doc.leftMargin = 72
        doc.rightMargin = 72
        doc.topMargin = 72
        doc.bottomMargin = 72

        image_path = os.path.join(settings.BASE_DIR, 'static', 'logo.png')
        image = Image(image_path, 80, 80)
        elements.append(image)
        elements.append(Paragraph("<para alignment='center'>Technological Elementary School</para>", styles['Heading2']))

        for student in queryset:
            # Header
            elements.append(Paragraph(f"Certificate of Registration", styles['Heading1']))
            elements.append(Paragraph(f"Student: {student.last_name}, {student.first_name}", styles['Normal']))
            elements.append(Paragraph(f"ID: {student.student_id}", styles['Normal']))
            elements.append(Paragraph(f"Section: {student.section}", styles['Normal']))
            
            # Schedule Table
            if hasattr(student, 'section') and student.section:
                schedule_data = [['Subject', 'Day', 'Time', 'Teacher']]
            for timeslot in student.section.schedules.all().first().time_slots.all():
                schedule_data.append([
                timeslot.subject.name,
                timeslot.get_day_display(),
                f"{timeslot.start_time} - {timeslot.end_time}",
                timeslot.teacher
                ])
            
            schedule_table = Table(schedule_data)
            schedule_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(schedule_table)
            elements.append(Paragraph(" ", styles['Normal']))  # Add space between entries
        
        doc.build(elements)
        return response
    def generate_enrollment_statistics(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="enrollment_statistics.pdf"'
        elements = []
        styles = getSampleStyleSheet()


        doc = SimpleDocTemplate(response, pagesize=letter)
        image_path = os.path.join(settings.BASE_DIR, 'static', 'logo.png')
        image = Image(image_path, 80, 80)
        elements.append(image)
        elements.append(Paragraph("<para alignment='center'>Technological Elementary School</para>", styles['Heading2']))

        
        # Get statistics
        total_students = Student.objects.count()
        stats_by_sex = Student.objects.values('sex').annotate(count=Count('id'))
        stats_by_grade = Student.objects.values('grade_level').annotate(count=Count('id'))
        
        # Create report
        elements.append(Paragraph("Enrollment Statistics Report", styles['Heading1']))
        elements.append(Paragraph(f"Total Enrolled Students: {total_students}", styles['Normal']))
        
        # Gender distribution table
        gender_data = [['Gender', 'Count']]
        for stat in stats_by_sex:
            gender_data.append([stat['sex'], stat['count']])
        
        gender_table = Table(gender_data)
        gender_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ]))
        elements.append(Paragraph("Distribution by Gender", styles['Heading2']))
        elements.append(gender_table)
        
        doc.build(elements)
        return response

    generate_cor.short_description = "Generate Certificate of Registration"
    generate_enrollment_statistics.short_description = "Generate Enrollment Statistics"




@admin.register(Student)
class StudentAdmin(RegistrarAdminMixin, admin.ModelAdmin):
    list_display = ('student_id', 'last_name', 'first_name', 'grade_level', 'status', 'enrollment_status')
    list_filter = ('status', 'enrollment_status', 'grade_level', 'academic_year', 'sex')
    search_fields = ('student_id', 'last_name', 'first_name', 'email')
    date_hierarchy = 'date_joined'
    actions = ['generate_cor']


@admin.register(Enrollment)
class EnrollmentAdmin(RegistrarAdminMixin, admin.ModelAdmin):
    list_display = ('student', 'student_type', 'grade_level', 'status', 'enrollment_date', 'kindergarten_certificate', 'transferee_report_card')
    list_filter = ('student_type', 'grade_level', 'status', 'academic_year')
    search_fields = ('student__last_name', 'student__first_name', 'student__student_id')
    date_hierarchy = 'enrollment_date'
    actions = ['generate_enrollment_statistics']

@admin.register(EnrollmentPeriod)
class EnrollmentPeriodAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date')
    list_filter = ('start_date', 'end_date')

class StudentInline(admin.TabularInline):
    model = Student
    extra = 1  

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('grade_level', 'section', 'academic_year', 'current_students', 'is_active')
    list_filter = ('grade_level', 'academic_year', 'is_active')
    search_fields = ('section', 'adviser__username')
    inlines = [StudentInline]

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('section', 'academic_year', 'is_active')
    list_filter = ('academic_year', 'is_active')
    search_fields = ('section__section',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'grade_level', 'units', 'is_active')
    list_filter = ('grade_level', 'is_active', 'units')
    search_fields = ('code', 'name', 'description')

class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = '__all__'
        widgets = {
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'end_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    form = TimeSlotForm
    list_display = ('day', 'start_time', 'end_time', 'subject', 'teacher')
    list_filter = ('day', 'schedule__academic_year', 'subject')
    search_fields = ('subject__name', 'teacher__username')

@admin.register(Mother)
class MotherAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'contact', 'occupation')
    search_fields = ('last_name', 'first_name', 'contact')
    list_filter = ('occupation', 'city', 'country')

@admin.register(Father)
class FatherAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'contact', 'occupation')
    search_fields = ('last_name', 'first_name', 'contact')
    list_filter = ('occupation', 'city', 'country')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('student', 'file_uploaded')
    search_fields = ('student__last_name', 'student__first_name', 'student__student_id')

@admin.register(ArchivedAccount)
class ArchivedAccountAdmin(admin.ModelAdmin):
    list_display = ('student', 'archived_on')
    list_filter = ('archived_on',)
    search_fields = ('student__last_name', 'student__first_name', 'student__student_id')
    date_hierarchy = 'archived_on'
