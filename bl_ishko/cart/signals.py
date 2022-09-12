from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from .models import Order


@receiver(pre_save, sender=Order)
def update_paid_status(**kwargs):
    if kwargs['instance'].paid and kwargs['instance'].is_active:
        pass



