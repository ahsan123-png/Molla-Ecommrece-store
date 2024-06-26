from django.db import models
from product.models import Product
from users.models import UserEx
# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(UserEx, on_delete=models.CASCADE)
    ordered_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    whole_total = models.DecimalField(max_digits=10, decimal_places=2,blank=True , null= True)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order #{self.id} - {self.ordered_product.product_name} by {self.customer.username}"



class Cancellation(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    user = models.ForeignKey(UserEx, on_delete=models.CASCADE)
    reason = models.TextField()
    cancellation_date = models.DateTimeField(auto_now_add=True)

class Shipment(models.Model):
    customer = models.ForeignKey(UserEx, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=20)
    delivery_status = models.CharField(max_length=50, default='Pending')
    shipping_date = models.DateField()
    estimated_delivery_date = models.DateField()
    actual_delivery_date = models.DateField(null=True, blank=True)
    shipment_address = models.ForeignKey('ShipmentAddress', on_delete=models.CASCADE,default=None)

    def __str__(self):
        return f"Shipment #{self.id} - Tracking: {self.tracking_number}, Status: {self.delivery_status}"

class ShipmentAddress(models.Model):
    orders = models.ManyToManyField(Order)
    customer = models.ForeignKey(UserEx, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    payment_method = models.CharField(max_length=30 , null=True,blank=True)
    email = models.EmailField()
    additional_note = models.TextField(blank=True)

# creating model for notifications

class Notification(models.Model):
    MESSAGE = 'Message'
    ORDER = 'Order'

    NOTIFICATION_TYPES = [
        (MESSAGE, 'Message'),
        (ORDER, 'Order'),
    ]

    message = models.TextField()
    type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
