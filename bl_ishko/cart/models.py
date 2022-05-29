import uuid

from django.db import models
from shop.models import Item
from django.conf import settings


PAYMENT_CHOICES = (
    ('CARD', 'Картой'),
    ('CASH', 'Наличными'),
)

DELIVERY_CHOICES = (
    ('NONE', 'Не выбран'),
    ('MOSCOW', 'Москва и МО'),
    ('CDEK', 'СДЭК'),
    ('POST_OFFICE', 'Почта России 1 класс'),
    ('ABROAD', 'Почтой за границу')
)


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
        return f'{self.item.id}.{self.item.product.title} {self.item.product.color} {self.item.size} - {self.quantity}'

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
        ordering = ['-created']


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order', verbose_name='Пользоатель')
    order_items = models.ManyToManyField(OrderItem, related_name='order')
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    ordered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False, verbose_name='Оплачен')

    def get_order_total_price(self):
        return sum([item.item_total() for item in self.order_items.all()])

    def get_order_total_price_with_sale(self):
        return round(sum([item.item_total_with_sale() for item in self.order_items.all()]), 1)

    def get_total_quantity(self):
        return sum([item.quantity for item in self.order_items.all()])

    def get_order_items_count(self):
        return self.order_items.all().count()

    def __str__(self):
        if self.ordered and self.is_active:
            if self.paid:
                order_status = 'Оплачен'
            else:
                order_status = 'Ожидает оплаты'
        elif self.ordered and not self.is_active:
            order_status = 'Выполнен'
        elif not self.ordered and self.is_active:
            order_status = 'В корзине'
        elif not self.ordered and not self.is_active:
            order_status = 'Отменен'
        return f'Заказ {self.id} от {self.user.email} - {order_status}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']


class BillingInfo(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='info', verbose_name='Заказ')
    first_name = models.CharField(max_length=60, verbose_name='Имя')
    last_name = models.CharField(max_length=60, verbose_name='Фамилия')
    country = models.CharField(default='Россия', max_length=50, blank=True, verbose_name='Страна')
    region = models.CharField(max_length=120, verbose_name='Регион')
    index = models.IntegerField(verbose_name='Почтовый индес')
    city = models.CharField(max_length=50, verbose_name='Город/Населенный пункт')
    address = models.CharField(max_length=256, verbose_name='Адрес')
    email = models.CharField(max_length=128, verbose_name='Email для заказа')
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    payment_method = models.CharField(choices=PAYMENT_CHOICES, max_length=10, verbose_name='Способ оплаты')
    delivery_type = models.CharField(choices=DELIVERY_CHOICES, max_length=30, verbose_name='Способ доставки', default='NONE')
    delivery_price = models.IntegerField(blank=True, null=True, verbose_name='Цена доставки')
    order_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Платежная информация - заказ № {self.order.id} ({self.order.user.email})'

    class Meta:
        verbose_name = 'Платежная информация о заказе'
        verbose_name_plural = 'Платежная ифнормация о заказах'

