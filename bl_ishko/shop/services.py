from django.db.models import Q

from .models import Product


def get_related_products_for_detail(product, count=6):
    id_already_in_use = []
    related_products = []

    # такие же продукты только другого цвета
    same_name_products = Product.objects.filter(Q(title=product.title) & ~Q(id=product.id))
    related_products.extend(same_name_products)
    id_already_in_use.extend([product.id for product in same_name_products])

    # продукты той же категории
    same_category_products = Product.objects.filter(~Q(id__in=id_already_in_use) & Q(category=product.category))
    related_products.extend(same_category_products)
    id_already_in_use.extend([product.id for product in same_category_products])

    if len(related_products) < count:
        related_products.extend(Product.objects.filter(~Q(id__in=id_already_in_use)).order_by('-created')[:count - len(related_products)])

    return related_products[:count]
