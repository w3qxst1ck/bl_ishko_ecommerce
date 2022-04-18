from django.db import models
from shop.models import Item
from django.conf import settings


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(default=1, verbose_name='Количество')

    def item_total(self):
        return self.quantity * self.item.product.price

    def __str__(self):
        return f'{self.item.id}.{self.item.product.title} - {self.quantity}'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='order')
    order_items = models.ManyToManyField(OrderItem)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    ordered = models.BooleanField(default=False)

    def get_order_total_price(self):
        return sum([item.item_total() for item in self.order_items.all()])

    def get_total_quantity(self):
        return sum([item.quantity for item in self.order_items.all()])

    def __str__(self):
        return f'{self.user.email}'

