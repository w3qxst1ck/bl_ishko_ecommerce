from django.db import models
from django.contrib.auth.models import User

from shop.models import Item


class WishItem(models.Model):
    wish_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='wishes', verbose_name='Товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Польователь')

