from django.db import models
from shop.models import Item
from django.conf import settings


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.item.product.title} - {self.quantity}'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='order')
    order_items = models.ManyToManyField(OrderItem)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.email}'

