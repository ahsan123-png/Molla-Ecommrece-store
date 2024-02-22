from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Add a URL pattern for the home view
    path('admin', views.adminDashboard, name='adminDashboard'),  # Add a URL pattern for the home view
    path('forms', views.adminForms, name='adminForms'),  # Add a URL pattern for the home view
    path('icons', views.adminIcons, name='adminIcons'),  # Add a URL pattern for the home view
    path('login', views.adminLogin, name='adminLogin'),  # Add a URL pattern for the home view
    path('profile', views.adminProfile, name='adminProfile'),  # Add a URL pattern for the home view
    path('register', views.adminRegister, name='adminRegister'),  # Add a URL pattern for the home view
    path('calender', views.adminCalender, name='adminCalender'),  # Add a URL pattern for the home view
    path('tables', views.adminTables, name='adminTables'),  # Add a URL pattern for the home view
    path('base', views.adminBase, name='adminBase'),  # Add a URL pattern for the home view
]