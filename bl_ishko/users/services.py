from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q


from .models import UserInfo
from shop.models import Product


def save_or_change_user_info(request):
    """Вносит изменения в модель User и UserInfo если их сделали"""
    user = get_object_or_404(User, id=request.user.id)
    user_info = get_object_or_404(UserInfo, user=user)
    query_post = request.POST
    for field in ['first_name', 'last_name']:
        if query_post[field] != getattr(user, field, None):
            setattr(user, field, query_post[field])
    for field in ['region', 'index', 'city', 'address', 'phone']:
        if query_post[field] != getattr(user_info, field, None):
            setattr(user_info, field, query_post[field])
    user.save()
    user_info.save()


def get_related_products(wish_products, count=6):
    related_products = []

    if wish_products:
        # выбираем id товаров которые уже в избранных
        id_already_in_use = set([wish_product.product.id for wish_product in wish_products])

        # выбираем товары подходящие и по цвету и по категории
        for wish_product in wish_products:
            category_and_color = Product.objects.filter(Q(category=wish_product.product.category) & Q(color=wish_product.product.color) & ~Q(id__in=id_already_in_use))
            # доабвляем id отбранных товаров в общее множество
            for product in category_and_color:
                id_already_in_use.add(product.id)
            # доабвляем товары в related products
            related_products.extend(category_and_color)

        if len(related_products) < count:
            for wish_product in wish_products:
                category_products = Product.objects.filter(Q(category=wish_product.product.category) & ~Q(id__in=id_already_in_use))
                for product in category_products:
                    id_already_in_use.add(product.id)
                related_products.extend(category_products)

        if len(related_products) < count:
            # id_already_in_related = list(id_already_in_related) + [product.id for product in related_products]
            random_products = Product.objects.filter(~Q(id__in=id_already_in_use)).order_by('-created')[:count - len(related_products)] #TODO со скидкой
            for product in random_products:
                id_already_in_use.add(product.id)
            related_products.extend(random_products)
    else:
        related_products.extend(Product.objects.all().order_by('-created')[:count])  #TODO выбирать со скидкой

    # минимально необходимое число продуктов
    if len(related_products) < 4:
        id_already_in_related = [product.id for product in related_products]
        related_products.extend(Product.objects.filter(~Q(id__in=id_already_in_related))[:4-len(related_products)])

    return related_products[:count]


