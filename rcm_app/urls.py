from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', home, name='home'),
    path('download-excel/', download_excel, name='download_excel'),
    path('download-pdf/', download_pdf, name='download_pdf'),
    path('dashboard/', dashboard_view, name='dashboard'),
    # path('test-verbose/', test_display_data_verbose, name='test-verbose'),
    path("register/", register_view, name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),

    path("upload_task/", upload_task_file, name="upload_task"),
    path('confirm_exceldata_import/', confirm_exceldata_import, name='confirm_exceldata_import'),

    path("upload/excel/", upload_excel, name="upload_excel"),
    path('map_excel_fields/', map_excel_fields, name='map_excel_fields'),
    path('excel/verbose/', excel_display_data_verbose, name='excel_display_data_verbose'),

    path('chat/<int:room_id>/', chat_room, name='chat_room'),
    path('send/', send_message, name='send_message'),
    path('start_chat/<int:user_id>/', start_chat, name='start_chat'),
    path('users/', user_list, name='user_list'),

    path('employee-targets/', employee_target_list, name='employee_target_list'),
    path('employee-targets/create/', employee_target_create, name='employee_target_create'),
    path('employee-targets/<int:pk>/update/', employee_target_update, name='employee_target_update'),
    path('employee-targets/<int:pk>/delete/', employee_target_delete, name='employee_target_delete'),
    path('employee-targets/dashboard/', employee_target_dashboard, name='employee_target_dashboard'),


    path('qa-audits/', qa_audit_list, name='qa_audit_list'),
    path('qa-audits/create/', qa_audit_create, name='qa_audit_create'),

    path('exceldata/edit/<int:pk>/', edit_exceldata, name='edit_exceldata'),
    path('exceldata/delete/<int:pk>/', delete_exceldata, name='delete_exceldata'),
]
