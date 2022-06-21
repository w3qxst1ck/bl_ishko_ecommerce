import os
from django.db.models import Prefetch

from cart.models import Order, OrderItem
from shop.models import Category, Product, Item


def get_order(request):
    if request.user.is_authenticated:
        # optimization
        item_qs = Item.objects.select_related('product')
        order_items_qs = OrderItem.objects.prefetch_related(Prefetch('item', queryset=item_qs))

        order = Order.objects.filter(user=request.user, ordered=False, is_active=True)\
            .prefetch_related(Prefetch('order_items', queryset=order_items_qs))
        if order.exists():
            order = order[0]
    else:
        order = None
    return {'order': order}


def get_categories(request):
    categories = Category.objects.all().order_by('-created').prefetch_related('products')
    return {'categories': categories}


def get_new_products(request):
    new_products = Product.objects.all().order_by('-created')[:4]
    return {'new_products': new_products}


def get_domain_name(request):
    domain_url = os.getenv('DOMAIN') + '/user/add_to_wishlist/'
    return {'domain_url': domain_url}
