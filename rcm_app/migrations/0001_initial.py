# Generated by Django 5.2.1 on 2025-06-09 11:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_name', models.CharField(max_length=100)),
                ('client_name', models.CharField(max_length=100, verbose_name='Client Name / Acc Name')),
                ('target', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ramp_percent', models.FloatField(default=0.0)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExcelUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('file_name', models.CharField(max_length=255)),
                ('row_count', models.PositiveIntegerField()),
                ('columns', models.JSONField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExcelData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(blank=True, max_length=100, null=True)),
                ('dos', models.DateField(blank=True, null=True, verbose_name='Date of Service')),
                ('dosym', models.CharField(blank=True, max_length=7, null=True)),
                ('run_number', models.CharField(blank=True, max_length=20, null=True)),
                ('inc_number', models.CharField(blank=True, max_length=20, null=True)),
                ('customer', models.CharField(blank=True, max_length=100, null=True)),
                ('dob', models.CharField(blank=True, max_length=10, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('prim_pay', models.CharField(blank=True, max_length=100, null=True)),
                ('pri_payor_category', models.CharField(blank=True, max_length=100, null=True)),
                ('cur_pay', models.CharField(blank=True, max_length=100, null=True)),
                ('cur_pay_category', models.CharField(blank=True, max_length=100, null=True)),
                ('schedule_track', models.CharField(blank=True, max_length=100, null=True)),
                ('event_step', models.CharField(blank=True, max_length=100, null=True)),
                ('coll', models.CharField(blank=True, max_length=10, null=True)),
                ('gross_charges', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('contr_allow', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('net_charges', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('revenue_adjustments', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('payments', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('write_offs', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('refunds', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('balance_due', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('aging_date', models.DateField(blank=True, null=True)),
                ('last_event_date', models.DateField(blank=True, null=True)),
                ('ordering_facility', models.CharField(blank=True, max_length=100, null=True)),
                ('vehicle', models.CharField(blank=True, max_length=50, null=True)),
                ('call_type', models.CharField(blank=True, max_length=50, null=True)),
                ('priority', models.CharField(blank=True, max_length=50, null=True)),
                ('call_type_priority', models.CharField(blank=True, max_length=100, null=True)),
                ('primary_icd', models.CharField(blank=True, max_length=20, null=True)),
                ('loaded_miles', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True)),
                ('pickup_facility', models.CharField(blank=True, max_length=100, null=True)),
                ('pickup_modifier', models.CharField(blank=True, max_length=10, null=True)),
                ('pickup_address', models.CharField(blank=True, max_length=255, null=True)),
                ('pickup_city', models.CharField(blank=True, max_length=100, null=True)),
                ('pickup_state', models.CharField(blank=True, max_length=2, null=True)),
                ('pickup_zip', models.CharField(blank=True, max_length=10, null=True)),
                ('dropoff_facility', models.CharField(blank=True, max_length=100, null=True)),
                ('dropoff_modifier', models.CharField(blank=True, max_length=10, null=True)),
                ('dropoff_address', models.CharField(blank=True, max_length=255, null=True)),
                ('dropoff_city', models.CharField(blank=True, max_length=100, null=True)),
                ('dropoff_state', models.CharField(blank=True, max_length=2, null=True)),
                ('dropoff_zip', models.CharField(blank=True, max_length=15, null=True)),
                ('import_date', models.DateField(blank=True, null=True)),
                ('import_date_ym', models.CharField(blank=True, max_length=7, null=True)),
                ('med_nec', models.CharField(blank=True, max_length=10, null=True)),
                ('accident_type', models.CharField(blank=True, max_length=50, null=True)),
                ('assigned_group', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('last_modified_date', models.DateField(blank=True, null=True)),
                ('last_modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('team', models.CharField(blank=True, max_length=100, null=True)),
                ('job', models.CharField(blank=True, max_length=50, null=True)),
                ('emsmart_id', models.CharField(blank=True, max_length=20, null=True)),
                ('prior_auth', models.CharField(blank=True, max_length=100, null=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rcm_app.employee')),
                ('upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='rcm_app.excelupload')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rcm_app.chatroom')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('company_email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('avg_claim_rate_per_month', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('heard_about_us', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
