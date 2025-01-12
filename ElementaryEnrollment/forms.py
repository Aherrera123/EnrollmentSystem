# forms.py
from django import forms
from .models import Student, Mother, Father, Document, Announcements
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
from .models import Enrollment  # Enrollment model to capture additional enrollment information
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class StudentForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    sex = forms.ChoiceField(choices=GENDER_CHOICES)

    class Meta:
        model = Student
        fields = [
            'student_id','last_name', 'first_name', 'middle_name', 'suffix', 'birth_date', 'sex', 'email',
            'street', 'barangay', 'city', 'state_province', 'country'  # New address fields for student
        ]
class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name','middle_name', 'last_name',  'email', 'street', 'barangay', 'city', 'state_province', 'country']

class MotherForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Mother
        fields = [
            'last_name', 'first_name', 'middle_name', 'contact', 'occupation', 'birth_date',
            'street', 'barangay', 'city', 'state_province', 'country'  # New address fields for mother
        ]

class FatherForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Father
        fields = [
            'last_name', 'first_name', 'middle_name', 'contact', 'occupation', 'birth_date',
            'street', 'barangay', 'city', 'state_province', 'country'  # New address fields for father
        ]

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file_uploaded']

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^TESP-\d{2}-\d{4}$',
                message='Username must be in format TESP-XX-XXXX where X is a digit',
                code='invalid_username'
            ),
        ],
        help_text='Format: TESP-XX-XXXX (e.g., TESP-23-0001)',
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
            'placeholder': 'TESP-23-0001'
        })
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
        }),
        help_text='• Must contain at least 8 characters<br>• Can\'t be similar to personal information<br>• Can\'t be entirely numeric'
    )

    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
        }),
        help_text='Enter the same password as before, for verification.'
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')
        
        # Check if username matches pattern
        if not re.match(r'^TESP-\d{2}-\d{4}$', username):
            raise ValidationError('Username must be in format TESP-XX-XXXX')
        
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        
        # Custom password validation
        if len(password) < 8:
            raise ValidationError('Password must contain at least 8 characters')
        
        if password.isdigit():
            raise ValidationError('Password cannot be entirely numeric')

        # Check for common passwords (you can expand this list)
        common_passwords = ['password', '12345678', 'qwerty123']
        if password.lower() in common_passwords:
            raise ValidationError('This password is too common')

        return password

class EnrollmentFormNewStudent(forms.ModelForm):
    kindergarten_certificate = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
            'accept': '.pdf,.jpg,.jpeg,.png',
            'id': 'kindergarten_certificate'
        }),
        help_text='Upload your Kindergarten completion certificate (PDF, JPG, PNG)'
    )
    student_type = forms.CharField(
        widget=forms.HiddenInput(),
        initial='new'
    )
    grade_level = forms.ChoiceField(
        choices=[('1', 'Grade 1')],
        initial='1',
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
        })
    )

    def clean_kindergarten_certificate(self):
        file = self.cleaned_data.get('kindergarten_certificate')
        if file:
            if file.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("File size must be under 5MB")
            return file
        return None

    class Meta:
        model = Enrollment
        fields = ['student_type', 'grade_level', 'kindergarten_certificate']

class EnrollmentFormTransferee(forms.ModelForm):
    transferee_report_card = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
            'accept': '.pdf,.jpg,.jpeg,.png',
            'id': 'transferee_report_card'
        })
    )
    student_type = forms.CharField(
        widget=forms.HiddenInput(),
        initial='transfer'
    )
    grade_level = forms.ChoiceField(
        choices=[
            ('1', 'Grade 1'),
            ('2', 'Grade 2'),
            ('3', 'Grade 3'),
            ('4', 'Grade 4'),
            ('5', 'Grade 5'),
            ('6', 'Grade 6'),
        ],
        widget=forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'})
    )
    previous_school = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'})
    )
    transfer_reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
            'rows': 3
        })
    )

    class Meta:
        model = Enrollment
        fields = ['student_type', 'grade_level', 'previous_school', 'transfer_reason', 'transferee_report_card']

#Admin----------------------
class CreateRegistrarForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcements
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'p-2 mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Enter announcement title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'p-2 mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'rows': 5,
                'placeholder': 'Write the announcement details here...'
            }),
        }