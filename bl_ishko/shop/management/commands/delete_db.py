from django.core.management.base import BaseCommand

from shop.models import Product, Category, ProductImages, Item


class Command(BaseCommand):
    help = 'Delete all data in DB'

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()
        ProductImages.objects.all().delete()
        Item.objects.all().delete()
        print('Все объекты успешно удалены из базы данных!')