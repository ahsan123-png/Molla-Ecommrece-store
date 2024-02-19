from django.urls import path
from . import views  # Import the home view

urlpatterns = [
    # path('cart', views.cart, name='cart'), 
    path('wishlist', views.wishlist, name='wishlist'), 
    path('cart', views.cart, name='cart'), 
    path('add_wishlist/', views.addToWishlist, name='add_to_wishlist'),
    path('add_to_cart/<int:id>', views.addCart, name='add_to_cart'),
    path('add_product_to_cart/<int:id>', views.addProductToCart, name='add_product_to_cart'),
    path('base', views.base, name='base') 
]
