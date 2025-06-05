# # rcm_app/urls.py
# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.home, name='home'),  # example URL pattern
# ]
from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_excel, name='upload_excel'),
    # path('display/', display_data, name='display_data'),
    # path('display_filtered/', display_filtered_data, name='display_filtered'),
    # path('test-display/', test_display_data, name='test_display_data'),
    path('download-excel/', download_excel, name='download_excel'),
    path('download-pdf/', download_pdf, name='download_pdf'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('test-verbose/', test_display_data_verbose, name='test-verbose'),
    path("register/", register_view, name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("upload/", upload_excel, name="upload"),
    path('chat/<int:room_id>/', chat_room, name='chat_room'),
    path('send/', send_message, name='send_message'),
    path('start_chat/<int:user_id>/', start_chat, name='start_chat'),
    path('users/', user_list, name='user_list'),

    path("upload_task/", upload_task_file, name="upload_task"),
    path('map_task_fields/', map_task_fields, name='map_task_fields'),
    path('confirm-import/', confirm_import, name='confirm_import'),

    path('employee-targets/', employee_target_list, name='employee_target_list'),
    path('employee-targets/create/', employee_target_create, name='employee_target_create'),
    path('employee-targets/<int:pk>/update/', employee_target_update, name='employee_target_update'),
    path('employee-targets/<int:pk>/delete/', employee_target_delete, name='employee_target_delete'),
    path('employee-targets/dashboard/', employee_target_dashboard, name='employee_target_dashboard'),
]
