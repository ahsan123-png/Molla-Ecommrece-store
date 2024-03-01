from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'), 
    path('shipment_address/', views.shipmentAddress, name='shipment_address'), 

]