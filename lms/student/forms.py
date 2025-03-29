from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from base.models import Student

# User Registration Form
class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_id', 'form', 'phone']

    def save(self, commit=True):
        # Create a new user with student_id as username
        user = User.objects.create_user(
            username=self.cleaned_data['student_id'],  # Use student_id as username
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student
# Login Form
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Student ID", widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        student_id = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if student_id and password:
            user = authenticate(self.request, username=student_id, password=password)
            if user is None:
                raise forms.ValidationError("Invalid student ID or password")

        return self.cleaned_data