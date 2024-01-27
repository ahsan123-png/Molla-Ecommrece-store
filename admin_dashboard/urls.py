from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name='home'),  # Add a URL pattern for the home view
]