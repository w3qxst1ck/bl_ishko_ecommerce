from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.utils import timezone
from shop.models import Product

from cart.models import OrderItem, Order
from shop.models import Item


@login_required
def cart_page(request):
    order_qs = Order.objects.filter(user=request.user, ordered=False, is_active=True)
    sold_out = False
    if order_qs.exists():
        if not is_enough_items(order_qs[0]):
            sold_out = True
    return render(request, 'cart/cart.html', context={'sold_out': sold_out})


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    input_size = request.GET.get('size')
    item = product.items.filter(size=input_size)[0]
    if item.item_count > 0:
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
        )
        order_qs = Order.objects.filter(user=request.user, is_active=True, ordered=False)
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
    else:
        redirect('shop:shop-page')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_from_cart(request, pk):
    order = get_object_or_404(Order, user=request.user, ordered=False, is_active=True)
    order_items = order.order_items.filter(id=pk)
    if order_items.exists():
        order_item = order_items[0]
        order.order_items.remove(order_item)
        order_item.delete()
    return redirect('cart:cart-page')


@login_required
def delete_all_from_cart(request):
    order = get_object_or_404(Order, user=request.user, ordered=False, is_active=True)
    order_items = order.order_items.all()
    if order_items.exists():
        order_items.delete()
    return redirect('cart:cart-page')


@login_required
def checkout_page(request):
    order_qs = Order.objects.filter(user=request.user, is_active=True, ordered=False)
    if order_qs.exists():
        if is_enough_items(order_qs[0]):
            return render(request, 'cart/checkout_page.html')
        else:
            return render(request, 'cart/sold_out.html')
    else:
        return HttpResponse('Заказ не существует')


@login_required
def order_complete_page(request):
    order = Order.objects.filter(user=request.user, is_active=True)[0]
    if is_enough_items(order):
        text = f'Заказ успешно офрмлен, его номер {order.id}. По указанному ' \
               f'номеру с вами свяяжется сотрудник, для подтверждения'
        send_message(text, request.user.email)  # TODO исправить мэйл, взять из формы
        for order_item in order.order_items.all():
            item = order_item.item
            item.item_count -= order_item.quantity
            item.save()
        order.ordered = True
        order.save()
        return render(request, 'cart/order_complete.html', context={'order': order})
    else:
        return HttpResponse('<h1>Ошибка в офрмлении заказа</h1>')   # TODO обработать нехватку товара


def send_message(text, client_email):
    pass


def is_enough_items(order):
    for order_item in order.order_items.all():
        if order_item.item.item_count < order_item.quantity:
            return False
    return True
