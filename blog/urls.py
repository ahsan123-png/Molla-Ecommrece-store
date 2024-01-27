from django.urls import path
from . import views  # Import the home view

urlpatterns = [
    path('blog', views.view, name='blog'), 
    path('review', views.review, name='review'), 

]
