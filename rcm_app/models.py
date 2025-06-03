from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from datetime import date


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
    # data = models.JSONField()

    company = models.CharField(max_length=100, default='Unknown')
    dos = models.DateField(verbose_name="Date of Service", default=date(2000, 1, 1))
    dosym = models.CharField(max_length=7, default='Unknown')
    run_number = models.CharField(max_length=20, default='Unknown')
    inc_number = models.CharField(max_length=20, default='Unknown')
    customer = models.CharField(max_length=100, null=True, blank=True)
    dob = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=50, default='Unknown')

    prim_pay = models.CharField(max_length=100, default='Unknown')
    pri_payor_category = models.CharField(max_length=100, default='Unknown')
    cur_pay = models.CharField(max_length=100, default='Unknown')
    cur_pay_category = models.CharField(max_length=100, default='Unknown')

    schedule_track = models.CharField(max_length=100, default='Unknown')
    event_step = models.CharField(max_length=100, default='Unknown')
    coll = models.CharField(max_length=10, default='NO')

    gross_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    contr_allow = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    net_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    revenue_adjustments = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payments = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    write_offs = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    refunds = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    aging_date = models.DateField(default=date(2000, 1, 1))
    last_event_date = models.DateField(default=date(2000, 1, 1))

    ordering_facility = models.CharField(max_length=100, null=True, blank=True)
    vehicle = models.CharField(max_length=50, default='Unknown')
    call_type = models.CharField(max_length=50, default='Unknown')
    priority = models.CharField(max_length=50, default='Unknown')
    call_type_priority = models.CharField(max_length=100, default='Unknown')

    primary_icd = models.CharField(max_length=20, default='Unknown')
    loaded_miles = models.DecimalField(max_digits=6, decimal_places=1, default=0.0)

    pickup_facility = models.CharField(max_length=100, null=True, blank=True)
    pickup_modifier = models.CharField(max_length=10, default='Unknown')
    pickup_address = models.CharField(max_length=255, null=True, blank=True)
    pickup_city = models.CharField(max_length=100, default='Unknown')
    pickup_state = models.CharField(max_length=2, default='NA')
    pickup_zip = models.CharField(max_length=10, default='00000')

    dropoff_facility = models.CharField(max_length=100, default='Unknown')
    dropoff_modifier = models.CharField(max_length=10, default='Unknown')
    dropoff_address = models.CharField(max_length=255, null=True, blank=True)
    dropoff_city = models.CharField(max_length=100, default='Unknown')
    dropoff_state = models.CharField(max_length=2, default='NA')
    dropoff_zip = models.CharField(max_length=15, default='00000')

    import_date = models.DateField(default=date(2000, 1, 1))
    import_date_ym = models.CharField(max_length=7, default='Unknown')

    med_nec = models.CharField(max_length=10, default='Unknown')
    accident_type = models.CharField(max_length=50, null=True, blank=True)

    assigned_group = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, default='Unknown')

    last_modified_date = models.DateField(default=date(2000, 1, 1))
    last_modified_by = models.CharField(max_length=100, default='Unknown')

    team = models.CharField(max_length=100, default='Unknown')
    job = models.CharField(max_length=50, default='Unknown')
    emsmart_id = models.CharField(max_length=20, default='Unknown')
    prior_auth = models.CharField(max_length=100, null=True, blank=True)

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
