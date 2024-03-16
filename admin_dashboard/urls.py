from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('home_dashboard', views.homeDashboard, name='home_dashboard'), 
    path('forms', views.adminForms, name='adminForms'), 
    path('admin_login', views.adminLogin, name='adminLogin'),  
    path('admin_register', views.adminRegister, name='adminRegister'),
    path('tables', views.adminTables, name='adminTables'),
    path('charts', views.adminChart, name='adminChart'),
]