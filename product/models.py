from django.db import models
from users.models import UserEx
# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    brand = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    stock = models.IntegerField()
    category = models.CharField(max_length=50)
    subcategory = models.CharField(max_length=50)




class ProductReview(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey(UserEx, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()

    # Customize the rating field with choices
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES)
    
    created_at = models.DateTimeField(auto_now_add=True)



class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField(default=0)