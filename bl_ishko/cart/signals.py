from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from .models import Order


@receiver(pre_save, sender=Order)
def update_paid_status(**kwargs):
    if kwargs['instance'].paid and kwargs['instance'].is_active:
        pass
    # print(kwargs['update_fields'])
    # if 'paid' in kwargs['update_fields']:
    #     print('Update')
        # if kwargs['instance'].paid == True:
        #     print('Пользователь оплатил заказ')
        # else:
        #     print('Отменил оплату')


