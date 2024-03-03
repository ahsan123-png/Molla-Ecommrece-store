from django.urls import path
from . import views  # Import the home view

urlpatterns = [
    path('card_pay', views.payment, name='card_pay'), 
    path('success', views.success, name='success'), 
    path('fail', views.failed, name='fail'), 

]
