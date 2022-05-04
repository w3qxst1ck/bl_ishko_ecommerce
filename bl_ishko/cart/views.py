from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from shop.models import Product

from cart.models import OrderItem, Order
from shop.models import Item


@login_required
def cart_page(request):
    order_qs = Order.objects.filter(user=request.user, is_active=True)
    if order_qs.exists():
        order = order_qs[0]
    else:
        order = None
    return render(request, 'cart/cart.html', context={'order': order})


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    input_size = request.GET.get('size')
    #try
    item = product.items.filter(size=input_size)[0]
    if item.item_count > 0:
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
        )
        order_qs = Order.objects.filter(user=request.user, is_active=True)
        if order_qs.exists():
            order = order_qs[0]
            if order.order_items.filter(item=item).exists():
                order_item.quantity += 1
                order_item.save()
            else:
                order.order_items.add(order_item)
        else:
            order = Order.objects.create(user=request.user)
            order.order_items.add(order_item)
        item.item_count -= 1
        item.save()
    else:
        redirect('shop:shop-page')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_from_cart(request, pk):
    # item = get_object_or_404(Item, id=pk)
    order = get_object_or_404(Order, user=request.user)
    order_items = order.order_items.filter(id=pk)
    if order_items.exists():
        order_item = order_items[0]
        # increase item count
        item = order_item.item
        item.item_count += order_item.quantity
        item.save()
        # delete order_item from order
        order.order_items.remove(order_item)
        order_item.delete()
    return redirect('cart:cart-page')


@login_required
def delete_all_from_cart(request):
    order = get_object_or_404(Order, user=request.user)
    order_items = order.order_items.all()
    if order_items.exists():
        # increase item count
        for order_item in order_items:
            item = order_item.item
            item.item_count += order_item.quantity
            item.save()
        # delete order_items from order
        order_items.delete()
    return redirect('cart:cart-page')
