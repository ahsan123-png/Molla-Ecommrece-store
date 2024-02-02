# In your app's urls.py file

from django.urls import path
from . import views  # Import the home view

urlpatterns = [
    path('', views.home, name='home'),  # Add a URL pattern for the home view
    path('signin', views.signin, name='signin'), 
    path('register', views.register, name='register'), 
    path('blog', views.blog, name='blog'), 
    path('about', views.about, name='about'), 
    path('contact', views.contact, name='contact'), 
    path('faq', views.faq, name='faq'), 
    path('coming_soon', views.coming_soon, name='coming_soon'), 
#========== curd api's =============
    path('all/users', views.all_users, name='all_users'), 
    path('<int:id>/get/user', views.get_user, name='get_user'), 

]
