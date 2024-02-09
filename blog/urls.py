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

# this static settingd are very import to display image on website
from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
    
    urlpatterns += static(
        settings.STATIC_URL, ## The URL for it
        document_root=settings.STATIC_ROOT ## the Folder
    )  ## FOR STATIC URL
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
