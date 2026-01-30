from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import file_views

urlpatterns = [
    path('', views.index, name='index'),
    path('formations/', views.formations, name='formations'),
    path('specialite/<slug:slug>/', views.specialite_detail, name='specialite_detail'),
    
    # URLs d'authentification
    path('login/', auth_views.LoginView.as_view(template_name='app_core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    
    # URLs pour la gestion des fichiers
    path('files/', file_views.file_manager_view, name='file_manager'),
    path('files/upload/', file_views.upload_file, name='upload_file'),
    path('files/<str:file_id>/download/', file_views.download_file, name='download_file'),
    path('files/<str:file_id>/delete/', file_views.delete_file, name='delete_file'),
    path('files/<str:file_id>/details/', file_views.file_details, name='file_details'),
    path('files/<str:file_id>/grant-access/', file_views.grant_access, name='grant_access'),
    path('files/logs/', file_views.access_logs, name='access_logs'),
]