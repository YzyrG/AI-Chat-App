from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('history', views.history, name='history'),
    path('delete_history/<history_id>', views.delete_history, name='delete_history'),
]
