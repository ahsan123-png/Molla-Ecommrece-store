from django.urls import path
from . import views  # Import the home view

urlpatterns = [
    path('blog', views.blog, name='blog'), 
    path('single', views.review, name='single'), 
    path('post/blog', views.post_blog, name='post_blog'), 
    path('upload', views.upload, name='upload'), 
    path('all_blogs', views.all_blogs, name='all_blogs'), 
    path('<int:id>/get_blog', views.get_blog, name='get_blog'), 
    path('<int:id>/update_blog', views.update_blog, name='update_blog'), 
    path('<int:id>/delete_blog', views.delete_blog, name='delete_blog'), 


]
