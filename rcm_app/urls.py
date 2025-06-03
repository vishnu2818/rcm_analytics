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

]
