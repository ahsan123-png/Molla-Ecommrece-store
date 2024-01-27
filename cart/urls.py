from django.urls import path
from . import views  # Import the home view

urlpatterns = [
    path('cart', views.cart, name='cart'), 
    path('wishlist', views.wishlist, name='wishlist'), 
]
