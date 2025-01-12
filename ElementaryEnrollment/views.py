from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import StudentForm, MotherForm, FatherForm, DocumentForm, EnrollmentFormNewStudent, EnrollmentFormTransferee
from .models import Student, Mother, Father, ArchivedAccount, EnrollmentPeriod
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Student, Enrollment, Schedule  # Assuming these models exist and are relevant
from django.utils import timezone
from .models import Enrollment
from .forms import StudentEditForm
from django.views.decorators.http import require_POST
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from .models import Announcements, Student
from .forms import AnnouncementForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
import pytz
from datetime import datetime

User = get_user_model()



def index(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard')
    else:
        return redirect('login')


@login_required
def student_profile(request):
    try:
        # Retrieve the Student record based on the logged-in user
        student = Student.objects.get(user=request.user)

        # Prepare the student data for the template
        student_data = {
            "id": student.id,  # Add the student ID here
            "student_id": student.student_id,
            "name": f"{student.first_name} {student.middle_name or ''} {student.last_name}",
            "birth_date": student.birth_date,
            "sex": student.sex,
            "email": student.email,
            "address": f"{student.street}, {student.barangay}, {student.city}, {student.state_province}, {student.country}",
        }
    except Student.DoesNotExist:
        # If no Student record is found for the user, set an error message
        student_data = {"error": "No student record found for this user."}

    # Render the profile template with the student data
    return render(request, 'Student_Profile.html', {"student_data": student_data})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # First, authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                # Check the student's approval status
                student = Student.objects.get(user_id=user.id)
                if student.status == 'Approved':
                    # If approved, log in the user
                    auth_login(request, user)
                    request.session.set_expiry(1800)  # 30 minutes
                    return redirect('student_dashboard')
                elif student.status == 'Rejected':
                    # If not approved, show an error message
                    messages.error(request, "Account has been rejected.")
                else:
                    # If not approved, show an error message
                    messages.error(request, "Account not approved yet.")
            except Student.DoesNotExist:
                messages.error(request, "No student profile associated with this user.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'LOGIN.html')


def enrollment_form_view(request):

    # Define the forms for initial loading or error cases
    form_new = EnrollmentFormNewStudent()
    form_transferee = EnrollmentFormTransferee()

    if request.method == 'POST':
        print("POST Data:", request.POST)
        student_type = request.POST.get('student_type')

        # Conditional handling based on student_type
        if student_type == "new":
            form = EnrollmentFormNewStudent(request.POST, request.FILES)
        elif student_type == "transfer":
            form = EnrollmentFormTransferee(request.POST, request.FILES)
        else:
            messages.error(request, "Invalid student type selected.")
            return render(request, 'ENROLLMENT_FORM.html', {'form_new': form_new, 'form_transferee': form_transferee})

        if form.is_valid():
            # For testing, confirm form data saved
            enrollment = form.save(commit=False)

            messages.success(request, "Enrollment form submitted successfully.")
            return redirect('student_dashboard')
        else:
            print("Form errors:", form.errors)  # Log form errors for debugging
            messages.error(request, "There was an issue with your submission. Please check your data.")

    return render(request, 'ENROLLMENT_FORM.html', {
        'form_new': form_new,
        'form_transferee': form_transferee
    })


# Registration Views
def registration_view(request):
    # Add this before creating form instances
    input_class = "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
    file_input_class = "mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"

    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        mother_form = MotherForm(request.POST, prefix='mother')
        father_form = FatherForm(request.POST, prefix='father')
        document_form = DocumentForm(request.POST, request.FILES)
        user_form = CustomUserCreationForm(request.POST)

        # Initialize enrollment forms
        enrollment_new_form = EnrollmentFormNewStudent()
        enrollment_transferee_form = EnrollmentFormTransferee()

        # Handle enrollment forms based on student type
        student_type = request.POST.get('student_type')
        if student_type == 'new':
            enrollment_form = EnrollmentFormNewStudent(request.POST, request.FILES)
            enrollment_new_form = enrollment_form
        elif student_type == 'transfer':
            enrollment_form = EnrollmentFormTransferee(request.POST, request.FILES)
            enrollment_transferee_form = enrollment_form
        else:
            # Handle invalid student type
            enrollment_form = None
            print("Invalid student type:", student_type)
            return render(request, 'REGISTRATION_FORM.html', {
                'error': 'Invalid student type selected',
                'student_form': student_form,
                'mother_form': mother_form,
                'father_form': father_form,
                'document_form': document_form,
                'user_form': user_form,
                'enrollment_new_form': enrollment_new_form,
                'enrollment_transferee_form': enrollment_transferee_form
            })

        if enrollment_form and all([
            student_form.is_valid(),
            mother_form.is_valid(),
            father_form.is_valid(),
            document_form.is_valid(),
            user_form.is_valid(),
            enrollment_form.is_valid()
        ]):
            # Convert date fields to strings for session storage
            user = user_form.save()

            student_data = student_form.save(commit=False)
            student_data.birth_date = student_data.birth_date.strftime('%Y-%m-%d')
            student_data.user = user
            year_suffix = str(datetime.now().year)[2:]
            user_pk = user.pk
            user_number = f"{user_pk:04d}"
            student_data.student_id = f"TESP-{year_suffix}-{user_number}"
            student_data.save()

            mother_data = mother_form.save(commit=False)
            mother_data.birth_date = mother_data.birth_date.strftime('%Y-%m-%d')
            mother_data.student = student_data
            mother_data.save()

            father_data = father_form.save(commit=False)
            father_data.birth_date = father_data.birth_date.strftime('%Y-%m-%d')
            father_data.student = student_data
            father_data.save()

            enrollment = enrollment_form.save(commit=False)
            enrollment.student = student_data
            enrollment.save()

            document = document_form.save(commit=False)
            document.student = student_data
            document.save()

            return redirect('login')
        else:
            print("Student Form Errors:", student_form.errors)
            print("Mother Form Errors:", mother_form.errors)
            print("Father Form Errors:", father_form.errors)
            print("Document Form Errors:", document_form.errors)
            print("User Form Errors:", user_form.errors)
            if enrollment_form:
                print("Enrollment Form Errors:", enrollment_form.errors)
    else:
        student_form = StudentForm()
        mother_form = MotherForm(prefix='mother')
        father_form = FatherForm(prefix='father')
        document_form = DocumentForm()
        user_form = CustomUserCreationForm()
        enrollment_new_form = EnrollmentFormNewStudent()
        enrollment_transferee_form = EnrollmentFormTransferee()

        # Update widget attributes for all forms
        for form in [student_form, mother_form, father_form]:
            for field in form.fields.values():
                if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.DateInput, forms.Select)):
                    field.widget.attrs.update({'class': input_class})
                elif isinstance(field.widget, forms.FileInput):
                    field.widget.attrs.update({'class': file_input_class})

        # Update document form separately
        for field in document_form.fields.values():
            field.widget.attrs.update({'class': file_input_class})

    return render(request, 'REGISTRATION_FORM.html', {
        'student_form': student_form,
        'mother_form': mother_form,
        'father_form': father_form,
        'document_form': document_form,
        'user_form': user_form,
        'enrollment_new_form': enrollment_new_form,
        'enrollment_transferee_form': enrollment_transferee_form
    })

def review(request):
    # Retrieve session data
    student_data = request.session.get('student_data')
    mother_data = request.session.get('mother_data')
    father_data = request.session.get('father_data')

    if not student_data or not mother_data or not father_data:
        return redirect('registration')

    if request.method == 'POST':
        if 'confirm' in request.POST:
            # Save data to the database upon confirmation
            student = Student.objects.create(
                **student_data,
                status ='Pending'  # Set default approval status to Pending
            )
            Mother.objects.create(student=student, **mother_data)
            Father.objects.create(student=student, **father_data)

            # Store the new student's ID in the session for later use
            request.session['student_id'] = student.id

            # Clear session data
            request.session.pop('student_data')
            request.session.pop('mother_data')
            request.session.pop('father_data')

            return redirect('create_account')
        elif 'back' in request.POST:
            return redirect('registration')

    return render(request, 'REVIEW.html', {
        'student_data': student_data,
        'mother_data': mother_data,
        'father_data': father_data
    })

def create_account(request):
   pass

# Additional Views
def enrollment_confirmation(request):
    return render(request, 'Email Confirmation.html')

def student_dashboard(request):
    return render(request, 'Student_Dashboard.html')

@login_required
def student_schedule(request):
    try:
        student = Student.objects.get(user=request.user)
        schedules = Schedule.objects.filter(section=student.section, is_active=True).prefetch_related('time_slots__subject', 'time_slots__teacher')
        return render(request, 'Student_Schedule.html', {'schedules': schedules})
    except Student.DoesNotExist:
        messages.error(request, "No student record found for this user.")
        return redirect('student_dashboard')

from django.utils import timezone

@login_required
def student_status(request):
    student = Student.objects.get(user=request.user)
    enrollment = Enrollment.objects.filter(student=student).first()

    # Calculate Passed Grades
    if enrollment.student_type == 'new':
        passed_grades = "Grade 1"
    elif enrollment.student_type == 'transfer':
        passed_grades = "Waiting For Evaluation"
    else:
        passed_grades = "N/A"

    # Determine current school year
    current_year = timezone.now().year
    school_year = f"{current_year}-{current_year + 1}"

    # Determine Status
    status = student.enrollment_status  # This assumes enrollment status tracks pending/approved/rejected

    context = {
        'passed_grades': passed_grades,
        'school_year': school_year,
        'status': status,
    }

    return render(request, 'Student_Status.html', context)


def student_requirements(request):
    print("Student Requirements")
    # Verify if current_date is within the records of EnrollmentPeriod
    now_utc  = timezone.now()
    manila_tz = pytz.timezone('Asia/Manila')
    current_date = now_utc.astimezone(manila_tz)
    print(current_date)
    enrollment_period = EnrollmentPeriod.objects.filter(start_date__lte=current_date, end_date__gte=current_date).first()
    if enrollment_period:
        print("Enrollment Period Found")
        return render(request, 'Student_Requirements.html')

    else:
        print("No Enrollment Period Found")
        return HttpResponse("Enrollment period is not available.")

def reset_password(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password')

        student = Student.objects.filter(confirmation_code=otp).first()
        if student:
            user = student.user
            print("User found:", user)
            print("New password:", new_password)

            user.set_password(new_password)
            user.save()
            student.confirmation_code = None
            student.save()
            print("Password reset successfully.")
            messages.success(request, "Password reset successfully.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP code.")
            return redirect('reset_password')

    elif request.method == "GET":
        otp = request.GET.get('otp')
        if not otp:
            return redirect('forgot_password')

        student = Student.objects.filter(confirmation_code=otp).first()
        if not student:
            messages.error(request, "Invalid OTP code.")
            return redirect('forgot_password')

        return render(request, 'Reset Password.html', {'otp': otp})

def forgot_password(request):
    return render(request, 'Forgot Password.html')

@login_required
def student_account(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user

        # Check if old password matches the current password
        if not check_password(old_password, user.password):
            messages.error(request, "Old password is incorrect.")
            return render(request, 'Student_Account.html')

        # Check if new password is the same as the old password
        if old_password == new_password:
            messages.error(request, "New password cannot be the same as the old password.")
            return render(request, 'Student_Account.html')

        # Check if new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return render(request, 'Student_Account.html')

        # Change the password
        user.set_password(new_password)
        user.save()

        # Update the session to prevent logout after password change
        update_session_auth_hash(request, user)

        messages.success(request, "Password successfully changed.")
        return redirect('student_account')

    return render(request, 'Student_Account.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def edit_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_profile')
        else:
            print(form.errors)
            return redirect('edit_profile', student_id=student_id)
    else:
        form = StudentEditForm(instance=student)

    return render(request, 'Edit_Profile.html', {'form': form, 'student': student})

@login_required
def create_announcement(request):
    if request.user.groups.filter(name__in=['Registrar', 'Superadmin']).exists():
        if request.method == 'POST':
            form = AnnouncementForm(request.POST)
            if form.is_valid():
                announcement = form.save(commit=False)
                announcement.author = request.user
                announcement.save()
                student_emails = Student.objects.values_list('email', flat=True)
                send_mail(
                    announcement.title,
                    announcement.content,
                    'admin@school.com',
                    student_emails,
                    fail_silently=False,
                )
                return redirect('create_announcement')  # or any preferred redirect
        else:
            form = AnnouncementForm()
        return render(request, 'RegistratAnnouncement.html', {'form': form})
    else:
        return redirect('login')



def email_confirmation(request):
    email = request.POST.get('email')
    try:
        student = Student.objects.get(email=email)
    except Student.DoesNotExist:
        student = None
    if student:
        messages.success(request, "An email has been sent to your email address. Please check your inbox.")

        otp_code = random.randint(100000, 999999)

        # Save the OTP code to the student object
        student.confirmation_code = otp_code
        student.save()

        # Send the OTP code via email with a link to the enrollment system
        send_mail(
            'Forgot Password OTP',
            f'Your OTP code is {otp_code}. Please use the following link to reset your password: '
            f'https://enrollmentsystem.pythonanywhere.com/reset_password?otp={otp_code}',
            'admin@school.com',
            [email],
            fail_silently=False,
        )

        return redirect('login')
    else:
        messages.error(request, "No student record found with this email.")
        return redirect('forgot_password')