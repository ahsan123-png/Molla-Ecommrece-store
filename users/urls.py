# In your app's urls.py file

from django.urls import path
from . import views  # Import the home view
from . import *
urlpatterns = [
    path('', views.home, name='home'),  # Add a URL pattern for the home view
    path('signin', views.signin, name='signin'), 
    path('register', views.register, name='register'), 
    path('logout', views.logout_view, name='logout'), 
    path('about', views.about, name='about'), 
    path('contact', views.contact, name='contact'), 
    path('faq', views.faq, name='faq'), 
    path('profile', views.profile, name='profile'), 
    path('coming_soon', views.coming_soon, name='coming_soon'), 
    path('404_Not_found', views.userNotFound, name='userNotFound'), 

#========== curd api's =============
    path('all/users', views.all_users, name='all_users'), 
    path('<int:id>/get/user', views.get_user, name='get_user'), 
    path('<int:id>/update', views.update, name='update'), 

]










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
