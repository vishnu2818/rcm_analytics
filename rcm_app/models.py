from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    company_name = models.CharField(max_length=100)
    company_email = models.EmailField()
    phone = models.CharField(max_length=15)
    avg_claim_rate_per_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    heard_about_us = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class ExcelUpload(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    row_count = models.PositiveIntegerField()
    columns = models.JSONField()

    def __str__(self):
        return f"{self.file_name} ({self.row_count} rows)"


class ExcelData(models.Model):
    upload = models.ForeignKey(ExcelUpload, on_delete=models.CASCADE, related_name='rows')
    company = models.CharField(max_length=100, null=True, blank=True)
    dos = models.DateField(null=True, blank=True, verbose_name="Date of Service")
    dosym = models.CharField(max_length=7, null=True, blank=True)
    run_number = models.CharField(max_length=20, null=True, blank=True)
    inc_number = models.CharField(max_length=20, null=True, blank=True)
    customer = models.CharField(max_length=100, null=True, blank=True)
    dob = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    prim_pay = models.CharField(max_length=100, null=True, blank=True)
    pri_payor_category = models.CharField(max_length=100, null=True, blank=True)
    cur_pay = models.CharField(max_length=100, null=True, blank=True)
    cur_pay_category = models.CharField(max_length=100, null=True, blank=True)
    schedule_track = models.CharField(max_length=100, null=True, blank=True)
    event_step = models.CharField(max_length=100, null=True, blank=True)
    coll = models.CharField(max_length=10, null=True, blank=True)
    gross_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    contr_allow = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    net_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    revenue_adjustments = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payments = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    write_offs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    refunds = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    balance_due = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    aging_date = models.DateField(null=True, blank=True)
    last_event_date = models.DateField(null=True, blank=True)
    ordering_facility = models.CharField(max_length=100, null=True, blank=True)
    vehicle = models.CharField(max_length=50, null=True, blank=True)
    call_type = models.CharField(max_length=50, null=True, blank=True)
    priority = models.CharField(max_length=50, null=True, blank=True)
    call_type_priority = models.CharField(max_length=100, null=True, blank=True)
    primary_icd = models.CharField(max_length=20, null=True, blank=True)
    loaded_miles = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    pickup_facility = models.CharField(max_length=100, null=True, blank=True)
    pickup_modifier = models.CharField(max_length=10, null=True, blank=True)
    pickup_address = models.CharField(max_length=255, null=True, blank=True)
    pickup_city = models.CharField(max_length=100, null=True, blank=True)
    pickup_state = models.CharField(max_length=2, null=True, blank=True)
    pickup_zip = models.CharField(max_length=10, null=True, blank=True)
    dropoff_facility = models.CharField(max_length=100, null=True, blank=True)
    dropoff_modifier = models.CharField(max_length=10, null=True, blank=True)
    dropoff_address = models.CharField(max_length=255, null=True, blank=True)
    dropoff_city = models.CharField(max_length=100, null=True, blank=True)
    dropoff_state = models.CharField(max_length=2, null=True, blank=True)
    dropoff_zip = models.CharField(max_length=15, null=True, blank=True)
    import_date = models.DateField(null=True, blank=True)
    import_date_ym = models.CharField(max_length=7, null=True, blank=True)
    med_nec = models.CharField(max_length=10, null=True, blank=True)
    accident_type = models.CharField(max_length=50, null=True, blank=True)
    assigned_group = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    last_modified_date = models.DateField(null=True, blank=True)
    last_modified_by = models.CharField(max_length=100, null=True, blank=True)
    team = models.CharField(max_length=100, null=True, blank=True)
    job = models.CharField(max_length=50, null=True, blank=True)
    emsmart_id = models.CharField(max_length=20, null=True, blank=True)
    prior_auth = models.CharField(max_length=100, null=True, blank=True)

    assigned_to = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Row from {self.upload.file_name}"


class ChatRoom(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room for: {', '.join(user.username for user in self.users.all())}"


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} at {self.timestamp}"


class Client(models.Model):
    PRICING_PLAN_CHOICES = [
        ('FTE', 'FTE-based'),
        ('Transaction', 'Per-Transaction'),
        ('Percentage', 'Percentage of Collections'),
        ('OldAR', 'Old AR Recovery')
    ]

    TYPE_CHOICES = [
        ('Provider', 'Healthcare Provider'),
        ('Billing', 'Billing Company'),
    ]

    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    specialty = models.CharField(max_length=100)
    start_date = models.DateField()
    avg_monthly_claims = models.PositiveIntegerField()
    avg_annual_claims = models.PositiveIntegerField()
    avg_claim_value = models.DecimalField(max_digits=10, decimal_places=2)
    pricing_plan = models.CharField(max_length=20, choices=PRICING_PLAN_CHOICES)
    plan_parameter = models.CharField(max_length=100)
    sla_target = models.CharField(max_length=100, blank=True, null=True)
    qa_target = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    employee_name = models.CharField(max_length=100)
    # client_name = models.CharField(max_length=100, verbose_name="Client Name / Acc Name")
    client_name = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client Name / Acc Name")
    target = models.DecimalField(max_digits=10, decimal_places=2)
    ramp_percent = models.FloatField(default=0.0)

    email = models.EmailField(unique=True, null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # more fields:
    joining_date = models.DateField(blank=True, null=True)
    designation = models.CharField(max_length=100,blank=True, null=True)
    sub_department = models.CharField(max_length=100, blank=True, null=True)
    ROLE_CHOICES = [
        ('Analyst', 'Analyst'),
        ('QA', 'QA'),
        ('Manager', 'Manager'),
        ('Admin', 'Admin'),
        ('Client', 'Client'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,blank=True, null=True)
    password_hash = models.CharField(max_length=255,blank=True, null=True)
    active = models.BooleanField(default=True,blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee_name} - {self.client_name}"


class SOW(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    department = models.CharField(max_length=100)
    default_sla = models.CharField(max_length=100, null=True, blank=True)
    default_qa_sampling = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SOWAssignment(models.Model):
    ROLE_CHOICES = [
        ('Primary', 'Primary Analyst'),
        ('Secondary', 'Backup Analyst'),
        ('QA', 'Quality Auditor')
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sow = models.ForeignKey(SOW, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    target_volume = models.PositiveIntegerField(null=True, blank=True)
    ramp_up_percent = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.client.name} - {self.sow.name} - {self.employee.employee_name}"


class QAAudit(models.Model):
    claim = models.ForeignKey(ExcelData, on_delete=models.CASCADE)
    audited_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='audits_done')
    audited_on = models.DateTimeField(auto_now_add=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    outcome = models.CharField(max_length=50, choices=[
        ('Pass', 'Pass'),
        ('Minor Error', 'Minor Error'),
        ('Major Error', 'Major Error'),
        ('Fail', 'Fail')
    ])
    error_type = models.CharField(max_length=100, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    rebuttal_status = models.CharField(max_length=20, choices=[
        ('None', 'None'),
        ('Disputed', 'Disputed'),
        ('Resolved', 'Resolved')
    ], default='None')
    rebuttal_comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Audit for Claim {self.claim.id} by {self.audited_by.employee_name}"
