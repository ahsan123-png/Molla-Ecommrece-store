from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('home_dashboard', views.homeDashboard, name='home_dashboard'), 
    path('dashboard_base', views.adminBase, name='dashboard_base'), 
    path('admin/notification/mark_read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('messages', views.messages, name='messages'), 
    path('admin_login', views.adminLogin, name='admin_login'),  
    path('admin_register', views.adminRegister, name='adminRegister'),
    path('orderList', views.orderList, name='orderList'),
    path('inventory', views.inventory, name='inventory'),
]