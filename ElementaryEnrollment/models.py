# models.py
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.mail import send_mail

class Student(models.Model):
    student_id = models.CharField(max_length=12, unique=True, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    suffix = models.CharField(max_length=10, blank=True)
    birth_date = models.DateField()
    sex = models.CharField(max_length=10)
    email = models.EmailField()
    date_joined = models.DateField(auto_now_add=True)
    academic_year = models.CharField(max_length=9, help_text="Format: YYYY-YYYY")
    semester = models.CharField(
        max_length=20,
        choices=[
            ('First', 'First Semester'),
            ('Second', 'Second Semester'),
            ('Summer', 'Summer')
        ],
        default='First'
    )

    # Student address fields
    street = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    grade_level = models.IntegerField(null=True, blank=True)
    section = models.ForeignKey('Section', on_delete=models.CASCADE, null=True, blank=True)
    # Track initial login and enrollment status
    first_login = models.BooleanField(default=True)  # True if first login
    enrollment_status = models.CharField(
        max_length=24,  # Adjusted to match the longest choice
        choices=[
            ('Pending Account Creation', 'Pending Account Creation'),
            ('Pending Enrollment', 'Pending Enrollment'),
            ('Enrolled', 'Enrolled')
        ],
        default='Pending Account Creation'
    )

    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    # forgot password fields 
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)   


    def __str__(self):  
        return f"{self.last_name}, {self.first_name} {self.middle_name} {self.student_id}"

    def save(self, *args, **kwargs):
        # Check if the status is changing to 'Regular'
        if self.pk is not None:
            print('Checking if status is changing to Regular')
            original = Student.objects.get(pk=self.pk)
            if original.status != 'Approved' and self.status == 'Approved':
                print('Student is now approved')
                try:
                    send_mail(
                        'Enrollment Accepted',
                        'Congratulations! Your account creation has been accepted, you can now login to the portal with your registered username and password.',
                        'admin@school.com',
                        [self.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(f"Failed to send email: {e}")
            else: 
                print('Student is not approved')
        # If student is approved and has no student_id, generate one
        if self.status == "Regular" and not self.student_id:
            current_year = datetime.datetime.now().year % 100  # Get last two digits of the year
            unique_number = Student.objects.filter(student_id__startswith=f"TESP-{current_year}").count() + 1
            self.student_id = f"TESP-{current_year}-{str(unique_number).zfill(4)}"
        super().save(update_fields=['status', 'student_id'] if 'status' in kwargs else None, *args, **kwargs)
        if self.section:
            self.section.save()
        
    def delete(self, *args, **kwargs):
        section = self.section
        archived_account = ArchivedAccount(student=self)
        archived_account.save()
        super().delete(*args, **kwargs)
        if section:
            section.save()
        
        
        
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_type = models.CharField(max_length=20, choices=[('new', 'New Student'), ('transfer', 'Transferee')])
    previous_school = models.CharField(max_length=255, blank=True, null=True)
    transfer_reason = models.TextField(blank=True, null=True)
    grade_level = models.CharField(max_length=20)
    kindergarten_certificate = models.FileField(upload_to='documents/', blank=True, null=True)
    transferee_report_card = models.FileField(upload_to='documents/', blank=True, null=True)
    academic_year = models.CharField(max_length=9, help_text="Format: YYYY-YYYY")
    enrollment_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )
    remarks = models.TextField(blank=True)
 
 
class EnrollmentPeriod(models.Model):   
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    def __str__(self):
        return f"{self.start_date} - {self.end_date}" 
 
        
class Mother(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    contact = models.CharField(max_length=20)
    occupation = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField()

    # Mother's address fields
    street = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='mother')

class Father(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    contact = models.CharField(max_length=20)
    occupation = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField()

    # Father's address fields
    street = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='father')

class Document(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    file_uploaded = models.FileField(upload_to='documents/')

class ArchivedAccount(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    archived_on = models.DateTimeField(auto_now_add=True)

class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday')
    ]
    
    section = models.ForeignKey('Section', on_delete=models.CASCADE, related_name='schedules')
    academic_year = models.CharField(max_length=9, help_text="Format: YYYY-YYYY")
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['section', 'academic_year']

    def __str__(self):
        return f"Schedule for {self.section} ({self.academic_year})"

class Section(models.Model): 
    grade_level = models.CharField(max_length=20)
    section = models.CharField(max_length=50)
    academic_year = models.CharField(max_length=9, help_text="Format: YYYY-YYYY")
    max_students = models.IntegerField(default=40)
    current_students = models.IntegerField(default=0, editable=False)
    adviser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['grade_level', 'section', 'academic_year']

    def __str__(self):
        return f"{self.grade_level} - {self.section} ({self.academic_year})"
    
    def save(self, *args, **kwargs):
        self.current_students = Student.objects.filter(section=self).count()
        super().save(*args, **kwargs)

class Subject(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    grade_level = models.CharField(max_length=20)
    units = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class TimeSlot(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='time_slots')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.CharField(max_length=3, choices=Schedule.DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ['schedule', 'day', 'start_time']
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.day} {self.start_time}-{self.end_time} {self.subject.code}"


class Announcements(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title