from django.db import models
from product.models import Product
from users.models import UserEx
from order.models import Order

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # user = models.ForeignKey(Userex, on_delete=models.CASCADE)
    
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} - Order #{self.order.id} by {self.user.username}"



class PurchaseHistory(models.Model):
    user = models.ForeignKey(UserEx, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
