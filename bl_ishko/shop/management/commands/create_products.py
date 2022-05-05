from django.core.management.base import BaseCommand
import json
import random
from mixer.backend.django import mixer
import os
from django.core.files import File


from shop.models import Product, Category, ProductImages, Item, FaqCategory, Faq


class Command(BaseCommand):
    help = 'Create Product with items and category in DB'
    CATEGORIES = ['Шорты', 'Футболки', 'Майки', 'Носки', 'Трусы', 'Аксессуары', 'Топики']
    FAQ_CATEGORIES = ['Основные', 'Возврат', 'Выбор размера', 'Доставка']

    def handle(self, *args, **options):
        count = 11
        self.create_categories()
        self.create_products(count)
        self.create_items(count * 5)
        self.create_images(count * 5)
        self.create_faqs_categories()
        self.create_faqs()

    @staticmethod
    def load_from_json(name):
        with open(f'shop/json/{name}.json', 'r') as file:
            objects = json.loads(file.read())
        return objects

    def create_categories(self):
        for category in self.CATEGORIES:
            Category.objects.create(
                title=category
            )
        print('Объекты Categories супешно созданы!')

    def create_products(self, count):
        all_images = os.listdir(path='shop/data/images/')
        for _ in range(count):
            mixer.blend(
                Product,
                title=mixer.FAKE,
                color=random.choice(['Red', 'BLue', 'Yellow', 'Black', 'Purple', 'Orange', 'Green', 'White']),
                category=mixer.SELECT,
                price=random.randint(100, 1000),
                slug=mixer.SKIP,
                discount=random.choice([0, 10, 20, 30]),
                is_active=True,
                title_image=File(open(f'shop/data/images/{all_images[random.randint(0, len(all_images)-1)]}', 'rb')),
                )
        print('Объекты Products супешно созданы!')

    def create_items(self, count):
        for _ in range(count):
            mixer.blend(
                Item,
                product=mixer.SELECT,
                item_count=random.randint(1, 6),
                size=random.choice(['XS', 'S', 'M', 'L', 'XL']),
            )
        # check duplicates
        all_items = Item.objects.all()
        all_products = Product.objects.all()
        for product in all_products:
            for size in ['XS', 'S', 'M', 'L', 'XL']:
                if len(all_items.filter(product=product, size=size)) > 1:
                    for item in all_items.filter(product=product, size=size)[1:]:
                        item.delete()

    def create_images(self, count):
        all_images = os.listdir(path='shop/data/images/')
        for i in range(0, count, 5):
            # gen = (img for img in all_images[i:i+5])
            mixer.cycle(5).blend(
                ProductImages,
                product=mixer.SELECT,
                image=File(open(f'shop/data/images/{all_images[i]}', 'rb')),
            )
        print('Фотографии товаров успешно созданы!')

    def create_faqs_categories(self):
        for category in self.FAQ_CATEGORIES:
            FaqCategory.objects.create(
                title=category
            )
        print('Объекты FAQCategory успешно созданы!')

    def create_faqs(self):
        categories = FaqCategory.objects.all()
        for category in categories:
            for _ in range(random.randint(2, 6)):
                mixer.blend(
                    Faq,
                    title=mixer.FAKE,
                    text=mixer.FAKE,
                    category=category
                )
        print('Объекты FAQs усупешно созданы!')