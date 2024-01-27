# In your app's urls.py file

from django.urls import path
from . import views  # Import the home view

urlpatterns = [
    path('lists', views.products, name='lists'), 
    path('detailed', views.product_details, name='detailed'), 
]
