from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from cart.models import OrderItem, Order
from shop.models import Item


@login_required
def cart_page(request):
    order = []
    try:
        order = Order.objects.get(user=request.user)
    except Order.DoesNotExist:
        pass
    return render(request, 'cart/cart.html', context={'order': order})


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, id=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item__id=pk).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.order_items.add(order_item)
    else:
        order = Order.objects.create(user=request.user)
        order.order_items.add(order_item)
    return redirect('cart:cart-page')


@login_required
def delete_from_cart(request, pk):
    # item = get_object_or_404(Item, id=pk)
    order = get_object_or_404(Order, user=request.user)
    if order.order_items.filter(item__id=pk).exists():
        order_item = OrderItem.objects.filter(item__id=pk, user=request.user)[0]
        order.order_items.remove(order_item)
        order_item.delete()
        return redirect('cart:cart-page')

    return redirect('cart:cart-page')