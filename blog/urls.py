from django.urls import path
from . import views  # Import the home view

urlpatterns = [
    path('blog', views.blog, name='blog'), 
    path('single', views.review, name='single'), 
    path('post/blog', views.post_blog, name='post_blog'), 
    path('upload', views.upload, name='upload'), 

]
