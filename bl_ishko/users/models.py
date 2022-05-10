from django.db import models
from django.contrib.auth.models import User

from shop.models import Product


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, null=True, blank=True)
    country = models.CharField(max_length=30, blank=True, default='Россия')
    region = models.CharField(max_length=127)
    city = models.CharField(max_length=127)
    index = models.CharField(max_length=6)
    address = models.CharField(max_length=255)


class WishProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishes', verbose_name='Товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    adding_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.product.title}'

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'


class ProductComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Пользователь')
    text = models.TextField()
    adding_date = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='Товар')

    def __str__(self):
        return f'{self.user.email} - {self.product.title}'

    class Meta:
        ordering = ['-adding_date']
        verbose_name = 'Комментарий к товару'
        verbose_name_plural = 'Комментарии к товарам'

