from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from shop.models import Product

from cart.models import OrderItem, Order, BillingInfo
from .services import is_enough_items, send_message_to_client, send_message_to_admin
from .tasks import send_messages_to_admin, send_messages_to_client


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
    # получение количества товара с фронтенда
    if request.GET.get('quantity'):
        input_quantity = int(request.GET.get('quantity'))
    else:
        input_quantity = 1

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
                order_item.quantity += input_quantity
                order_item.save()
            else:
                order_item.quantity = input_quantity
                order_item.save()
                order.order_items.add(order_item)
        else:
            order = Order.objects.create(user=request.user)
            order_item.quantity = input_quantity
            order_item.save()
            order.order_items.add(order_item)
    else:
        redirect('shop:shop-page')

    if request.META.get('HTTP_REFERER').split('/')[-2] == 'search':
        return redirect('cart:cart-page')
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
        if order_qs[0].order_items.all():
            if is_enough_items(order_qs[0]):
                return render(request, 'cart/checkout_page.html')
            else:
                return render(request, 'cart/sold_out.html')
        else:
            return render(request, 'cart/empty_order.html')
    else:
        return HttpResponse('Заказ не существует')


@login_required
def order_complete_page_intermediate(request):
    order = Order.objects.filter(user=request.user, is_active=True)[0]
    if is_enough_items(order):
        for order_item in order.order_items.all():
            item = order_item.item
            item.item_count -= order_item.quantity
            item.save()
        order.ordered = True
        order.save()

        # сохранение доп информации
        create_billing_info(request, order)

        # оповещение клиента
        send_messages_to_client.delay(order.id)

        # оповещение администратора
        send_messages_to_admin.delay(request.user.email, order.id)

        return redirect('cart:order-complete-page', uuid=order.id)
    else:
        return render(request, 'cart/sold_out.html')


def create_billing_info(request, order):
    billing_info = BillingInfo.objects.create(
        order=order,
        first_name=request.GET.get('first-name'),
        last_name=request.GET.get('last-name'),
        region=request.GET.get('region'),
        index=request.GET.get('postal-code'),
        city=request.GET.get('city'),
        address=request.GET.get('address'),
        email=request.GET.get('email'),
        phone=request.GET.get('phone'),
        order_comment=request.GET.get('order-message')
    )
    if request.GET.get('card_payment'):
        billing_info.payment_method = 'CARD'
    if request.GET.get('cash_payment'):
        billing_info.payment_method = 'CASH'
    billing_info.save()


@login_required
def order_complete_page(request, uuid):
    order = Order.objects.get(id=uuid)
    return render(request, 'cart/order_complete.html', context={'order': order})


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # изменение статуса заказа
    order.ordered = False
    order.is_active = False
    order.save()
    # изменение количества товара на складе
    for order_item in order.order_items.all():
        item = order_item.item
        item.item_count += order_item.quantity
        item.save()
    # оповещение администратора
    send_messages.delay(request, order, 'admin', canceled=True)
    # оповещение клиента
    send_messages.delay(request, order, 'client', canceled=True)
    return redirect('users:profile-orders-page')


@login_required
def cancel_order_confirm(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'users/cancel_order_confirm.html', {'order': order})


