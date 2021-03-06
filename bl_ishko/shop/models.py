from django.db import models
from django.utils.text import slugify
from .utils import alphabet
from time import time


def gen_slug(title, model_type=None):
    if model_type:
        eng_title = ''.join(alphabet.get(c, c) for c in title.lower())
        slug_field = ' '.join(eng_title.split()[:4]) + '-' + str(time())[-3:]
    else:
        slug_field = ''.join(alphabet.get(c, c) for c in title.lower())
    return slugify(slug_field, allow_unicode=True)


CHOICES = (
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
)


class Product(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Название')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    price = models.FloatField(verbose_name='Цена')
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    discount = models.IntegerField(blank=True, null=True, verbose_name='Скидка')
    description = models.TextField(verbose_name='Опсиание')
    compound = models.TextField(verbose_name='Состав')
    care = models.TextField(verbose_name='Уход')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title, model_type='product')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items', verbose_name='Продукт')
    item_count = models.IntegerField(verbose_name='Количество товара')
    size = models.CharField(choices=CHOICES, max_length=10, blank=True, null=True, verbose_name='Размер')
    color = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.product.title} - {self.color} ({self.size}) - {self.item_count} шт.'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Фото товара', related_name='images')
    image = models.ImageField(upload_to='products/')


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
