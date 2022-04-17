from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from cart.models import OrderItem, Order
from shop.models import Item


def cart_page(request):
    return render(request, 'cart/cart.html')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, product__slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item__product__slug=slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.order_items.add(order_item)
    else:
        order = Order.objects.create(user=request.user)
        order.order_items.add(order_item)
    return redirect('cart:cart-page')

