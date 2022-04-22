from django.db import models
from django.contrib.auth.models import User

from shop.models import Product


class WishProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishes', verbose_name='Товар', unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Польователь')

    def __str__(self):
        return f'{self.user.email} - {self.product.title}'

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'


