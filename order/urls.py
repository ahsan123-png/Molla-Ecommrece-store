from django.urls import path
from . import views

urlpatterns = [
    path('checkout', views.chcekout, name='checkout'), 
    path('shipment', views.shipment_address, name='shipment'), 

]