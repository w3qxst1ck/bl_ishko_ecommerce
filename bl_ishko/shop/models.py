from django.db import models
from .utils import gen_slug
from django.shortcuts import reverse
from datetime import datetime, timedelta

from django.contrib.auth.models import User


CHOICES = (
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
)


class Product(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Название')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='products', verbose_name='Категория')
    color = models.CharField(max_length=128, verbose_name='Цвет')
    price = models.FloatField(verbose_name='Цена')
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    discount = models.IntegerField(blank=True, null=True, verbose_name='Скидка')
    description = models.TextField(verbose_name='Опсиание')
    compound = models.TextField(verbose_name='Состав')
    care = models.TextField(verbose_name='Уход')
    title_image = models.ImageField(upload_to='products/title_images', verbose_name='Главная картинка')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title, model_type='product')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:detail-page', kwargs={'slug': self.slug})

    def get_price(self):
        if self.discount:
            return round(self.price - self.price * 0.01 * self.discount, 1)
        return self.price

    def is_new(self):
        delta = timedelta(days=30)
        return True if self.created - datetime.now() < delta else False

    def __str__(self):
        return f'{self.title} - {self.color}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created']


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items', verbose_name='Продукт')
    item_count = models.IntegerField(verbose_name='Количество товара')
    size = models.CharField(choices=CHOICES, max_length=10, blank=True, null=True, verbose_name='Размер')

    def __str__(self):
        return f'{self.product.title} ({self.size}) - {self.item_count} шт.'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['product__title',]


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Фото товара', related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f'{self.id}. {self.product.title} - {self.product.color}'

    class Meta:
        verbose_name = 'Фото продукта'
        verbose_name_plural = 'Фото продуктов'
        ordering = ['product__title']


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField()
    image = models.ImageField(upload_to='categories/', verbose_name='Изображение')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:cat-shop-page', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'
        ordering = ['title']


class FaqCategory(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Название категории')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:faq-page', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'Категория FAQ'
        verbose_name_plural = 'Категории FAQ'


class Faq(models.Model):
    title = models.TextField(verbose_name='Вопрос', db_index=True)
    text = models.TextField(verbose_name='Ответ', db_index=True)
    category = models.ForeignKey(FaqCategory, on_delete=models.CASCADE, related_name='faqs', verbose_name='Категория')

    def __str__(self):
        return f'{self.category.title} - {self.title}'

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'


class Post(models.Model):
    category = models.CharField(max_length=512, verbose_name='Тема поста')
    title = models.CharField(max_length=512, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст поста')
    image = models.ImageField(upload_to='posts/', verbose_name='Постер')
    date = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=125, default='admin', verbose_name='Автора поста', blank=True)
    is_active = models.BooleanField(default=False, verbose_name='Активный')

    def __str__(self):
        return f'{self.author} - "{self.title}"'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-date']
