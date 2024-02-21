from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Add a URL pattern for the home view
    path('admin', views.adminDashboard, name='adminDashboard'),  # Add a URL pattern for the home view
]