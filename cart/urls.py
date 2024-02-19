from django.urls import path
from . import views  # Import the home view

urlpatterns = [
    path('cart', views.cart, name='cart'), 
    path('wishlist', views.wishlist, name='wishlist'), 
    path('add_wishlist/', views.addToWishlist, name='add_to_wishlist'),
    path('base', views.base, name='base') 
]
