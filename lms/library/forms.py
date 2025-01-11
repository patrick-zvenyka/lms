from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class ProfilePasswordChangeForm(PasswordChangeForm):
    # Customize the form if needed (optional)
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput)
