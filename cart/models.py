from django.db import models

# Create your models here.
from django.db import models
from users.models import UserEx
from product.models import Product



class Cart(models.Model):
    user = models.ForeignKey(UserEx, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s Cart - {self.product.product_name}"




class Wishlist(models.Model):
    user = models.ForeignKey(UserEx, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=20,default="unknown",null=True, blank=True)  # Add color field
    size = models.CharField(max_length=10,default="unknown",null=True, blank=True)   # Add size field
    quantity = models.IntegerField(default=1) 

    def __str__(self):
        return f"{self.user.username}'s Wishlist - {self.product.product_name}"