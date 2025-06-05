# rcm_app/forms.py
from django.contrib.auth.models import User
from django import forms
from .models import EmployeeTarget


class ExcelUploadForm(forms.Form):
    file = forms.FileField()


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    company_name = forms.CharField(max_length=100)
    company_email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    avg_claim_rate_per_month = forms.DecimalField(max_digits=10, decimal_places=2)
    heard_about_us = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'company_name', 'company_email', 'phone', 'avg_claim_rate_per_month',
                  'heard_about_us']


class EmployeeTargetForm(forms.ModelForm):
    class Meta:
        model = EmployeeTarget
        fields = ['employee_name', 'client_name', 'target', 'ramp_percent']