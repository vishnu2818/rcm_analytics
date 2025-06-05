from django.contrib import admin
from .models import ExcelUpload, ExcelData
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth.models import User
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'company_email', 'phone', 'avg_claim_rate_per_month', 'heard_about_us')


admin.site.register(Profile, UserProfileAdmin)
admin.site.register(ExcelData)
admin.site.register(ExcelUpload)
admin.site.register(EmployeeTarget)


# class ExcelDataInline(admin.TabularInline):
#     model = ExcelData
#     extra = 0
#     readonly_fields = ('data_preview',)
#     fields = ('data_preview',)
#
#     def data_preview(self, obj):
#         preview = "<table class='table'><tr><th>Field</th><th>Value</th></tr>"
#         for k, v in obj.data.items():
#             preview += f"<tr><td>{k}</td><td>{v if v is not None else ''}</td></tr>"
#         preview += "</table>"
#         return format_html(preview)
#
#     data_preview.short_description = "Data Preview"
#
#
# @admin.register(ExcelUpload)
# class ExcelUploadAdmin(admin.ModelAdmin):
#     list_display = ('file_name', 'uploaded_at', 'row_count')
#     readonly_fields = ('columns_preview',)
#     inlines = [ExcelDataInline]
#
#     def columns_preview(self, obj):
#         return format_html("<br>".join(obj.columns.keys()))
#
#     columns_preview.short_description = "Columns"
#
#
# @admin.register(ExcelData)
# class ExcelDataAdmin(admin.ModelAdmin):
#     list_display = ('id', 'upload_link', 'data_preview')
#     list_filter = ('upload',)
#     readonly_fields = ('data_display',)
#     fields = ('upload', 'data_display')
#
#     def upload_link(self, obj):
#         return format_html(
#             '<a href="{}">{}</a>',
#             f'/admin/rcm_app/excelupload/{obj.upload.id}/change/',
#             obj.upload.file_name
#         )
#
#     upload_link.short_description = "Upload"
#     upload_link.admin_order_field = 'upload'
#
#     def data_preview(self, obj):
#         preview_items = list(obj.data.items())[:3]  # Show first 3 fields
#         return format_html("<br>".join(
#             f"<b>{k}:</b> {v if v is not None else ''}"
#             for k, v in preview_items
#         ))
#
#     data_preview.short_description = "Data Preview"
#
#     def data_display(self, obj):
#         table = "<table class='table'><tr><th>Field</th><th>Value</th></tr>"
#         for k, v in obj.data.items():
#             table += f"<tr><td>{k}</td><td>{v if v is not None else ''}</td></tr>"
#         table += "</table>"
#         return format_html(table)
#
#     data_display.short_description = "Data"
