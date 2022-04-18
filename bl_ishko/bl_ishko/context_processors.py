from cart.models import Order
from shop.models import Category


def get_order(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user)
        if order.exists():
            order = order[0]
    else:
        order = None
    return {'order': order}


def get_categories(request):
    categories = Category.objects.all().order_by('title')
    return {'categories': categories}

