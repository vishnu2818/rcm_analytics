# rcm_app/forms.py
from django.contrib.auth.models import User
from django import forms
from .models import Employee, ExcelData


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


class EmployeeForm(forms.ModelForm):
    tasks = forms.ModelMultipleChoiceField(
        queryset=ExcelData.objects.filter(assigned_to__isnull=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Assign Tasks"
    )

    class Meta:
        model = Employee
        fields = [
            'employee_name', 'client_name', 'target', 'ramp_percent',
            'email', 'department', 'joining_date', 'designation',
            'sub_department', 'role', 'active', 'notes', 'tasks'
        ]


from .models import QAAudit
from django import forms


class QAAuditForm(forms.ModelForm):
    class Meta:
        model = QAAudit
        fields = [
            'claim',
            'score',
            'audited_by',
            'outcome',
            'error_type',
            'comments',
            'rebuttal_status',
            'rebuttal_comments',
        ]


from django.forms.widgets import DateInput


class ExcelDataForm(forms.ModelForm):
    class Meta:
        model = ExcelData
        exclude = ['upload']
        widgets = {
            'dos': DateInput(attrs={'type': 'date'})
        }
