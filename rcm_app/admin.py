# from django.contrib import admin
# from .models import ExcelUpload, ExcelData
# from django.utils.html import format_html
# from django.contrib import admin
# from django.contrib.auth.models import User
# from .models import *
#
#
# @admin.register(Profile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'company_name', 'company_email', 'phone', 'avg_claim_rate_per_month', 'heard_about_us')
#
#
# @admin.register(ExcelData)
# class ExcelDataAdmin(admin.ModelAdmin):
#     list_display = ('company', 'assigned_to', 'status')
#     list_filter = ('assigned_to', 'status')
#     search_fields = ('assigned_to__employee_name', 'customer', 'company')
#
#
# @admin.register(Client)
# class ClientAdmin(admin.ModelAdmin):
#     list_display = ('name', 'type', 'pricing_plan', 'active')
#     search_fields = ('name', 'specialty')
#     list_filter = ('type', 'pricing_plan', 'active')
#
#
#
#
# # admin.site.register(Profile, UserProfileAdmin)
# admin.site.register(ExcelUpload)
# admin.site.register(Employee)


from django.contrib import admin
from .models import *


# @admin.register(Profile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'company_name', 'company_email', 'phone', 'avg_claim_rate_per_month', 'heard_about_us')
#

@admin.register(ExcelUpload)
class ExcelUploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'file_name', 'row_count', 'uploaded_at')


@admin.register(ExcelData)
class ExcelDataAdmin(admin.ModelAdmin):
    list_display = ('company', 'assigned_to', 'status', 'dos', 'prim_pay', 'balance_due', 'prior_auth', )
    list_filter = ('assigned_to', 'status', 'prim_pay')
    search_fields = ('customer', 'company', 'assigned_to__employee_name')


# @admin.register(ChatRoom)
# class ChatRoomAdmin(admin.ModelAdmin):
#     list_display = ('id', 'created_at')
#

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender', 'timestamp', 'content')
    search_fields = ('sender__username', 'content')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'specialty', 'pricing_plan', 'qa_target', 'active')
    search_fields = ('name', 'specialty')
    list_filter = ('type', 'pricing_plan', 'active')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'client_name', 'role', 'target', 'ramp_percent', 'department', 'active')
    list_filter = ('role', 'active', 'client_name')
    search_fields = ('employee_name', 'email')


@admin.register(SOW)
class SOWAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'default_sla', 'default_qa_sampling', 'active')
    search_fields = ('name',)
    list_filter = ('department', 'active')


@admin.register(SOWAssignment)
class SOWAssignmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'sow', 'employee', 'role', 'target_volume', 'ramp_up_percent', 'start_date', 'end_date')
    list_filter = ('client', 'sow', 'role')
    search_fields = ('employee__employee_name', 'client__name', 'sow__name')


from .models import QAAudit

@admin.register(QAAudit)
class QAAuditAdmin(admin.ModelAdmin):
    list_display = ('claim', 'audited_by', 'score', 'outcome', 'audited_on')
    search_fields = ('claim__customer', 'audited_by__employee_name', 'error_type')
    list_filter = ('outcome', 'rebuttal_status')
