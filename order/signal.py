from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Order, Notification

@receiver(post_save, sender=Order)
def order_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            message=f'New order placed: {instance.id}',
            type=Notification.ORDER,
            created_at=timezone.now()
        )
    else:
        Notification.objects.create(
            message='New customer message',
            type=Notification.MESSAGE,
            created_at=timezone.now()
        )
