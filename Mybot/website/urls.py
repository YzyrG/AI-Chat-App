from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('delete_history/<history_id>', views.delete_history, name='delete_history'),
    path('writing_history/', views.writing_history, name='writing_history'),
    path('delete_writing/<writing_id>', views.delete_history, name='delete_writing'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
]
