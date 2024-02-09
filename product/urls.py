# In your app's urls.py file

from django.urls import path
from . import views  # Import the home view

urlpatterns = [
    path('lists', views.products, name='lists'), 
    path('detailed', views.product_details, name='detailed'), 
    path('add', views.add, name='add'), 
    path('add_product', views.addProduct, name='add_product'), 
    # ==== CURD =====
    path('get_all', views.allProduct, name='allProduct'), 
    path('get_product/<int:id>', views.getProduct, name='getProduct'), 
    path('update/<int:id>', views.updateProduct, name='updateProduct'), 
    path('delete/<int:id>', views.deleteProduct, name='deleteProduct'), 
]
