from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Notification


def order_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            message=f'New order placed: {instance.order_id}',
            type=Notification.ORDER
        )