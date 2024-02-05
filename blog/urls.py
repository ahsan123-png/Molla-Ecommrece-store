from django.urls import path
from . import views  # Import the home view

urlpatterns = [
    path('blog', views.blog, name='blog'), 
    path('single', views.review, name='single'), 

]
