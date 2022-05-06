import uuid

from django.db import models
from shop.models import Item
from django.conf import settings


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(default=1, verbose_name='Количество')
    created = models.DateTimeField(auto_now_add=True)

    def item_total(self):
        return self.quantity * self.item.product.price

    def item_total_with_sale(self):
        item_total = self.item_total()
        if self.item.product.discount:
            item_total = item_total - item_total * self.item.product.discount / 100
        return round(item_total, 1)

    def __str__(self):
        return f'{self.item.id}.{self.item.product.title} - {self.quantity}'

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
        ordering = ['-created']


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='order')
    order_items = models.ManyToManyField(OrderItem)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    ordered = models.BooleanField(default=False)

    def get_order_total_price(self):
        return sum([item.item_total() for item in self.order_items.all()])

    def get_order_total_price_with_sale(self):
        return round(sum([item.item_total_with_sale() for item in self.order_items.all()]), 1)

    def get_total_quantity(self):
        return sum([item.quantity for item in self.order_items.all()])

    def get_order_items_count(self):
        return self.order_items.all().count()

    def __str__(self):
        if self.ordered:
            ordered = 'Выполнен'
        else:
            ordered = 'Не выполнен'
        return f'{self.id}. {self.user.email} - {ordered}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']

