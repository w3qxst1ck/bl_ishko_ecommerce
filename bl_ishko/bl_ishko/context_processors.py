from cart.models import Order
from shop.models import Category, Product


def get_order(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, ordered=False, is_active=True)
        if order.exists():
            order = order[0]
    else:
        order = None
    return {'order': order}


def get_categories(request):
    categories = Category.objects.all().order_by('title')
    all_products = Product.objects.all()
    colors = sorted(list(set([product.color for product in all_products])))
    colors_tuple_list = []
    for color in colors:
        product_count = all_products.filter(color=color).count()
        colors_tuple_list.append((color, product_count))
    return {'categories': categories, 'colors_tuple_list': colors_tuple_list}


def get_new_products(request):
    new_products = Product.objects.all().order_by('-created')[:4]
    return {'new_products': new_products}
