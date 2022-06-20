from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from loguru import logger
import json
import os

from shop.models import Product, Item
from cart.models import OrderItem, Order, BillingInfo
from .services import is_enough_items
from .tasks import send_messages_to_admin, send_messages_to_client


@login_required
def cart_page(request):
    # optimization
    order_item_qs = OrderItem.objects.select_related('item')

    order_qs = Order.objects.filter(user=request.user, ordered=False, is_active=True).prefetch_related(Prefetch('order_items', queryset=order_item_qs))
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
        if input_quantity == 0:
            return redirect('shop:shop-page')
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

        logger.warning(f'Пользователь с Email: {request.user.email} пытался добавить в корзину товар "{item.product.title}",которого нет в наличии, '
                    f'размер: {item.size} цвет: {item.product.color} количество: {input_quantity}')

        redirect('shop:shop-page')

    if request.META.get('HTTP_REFERER').split('/')[-2] == 'search':

        logger.info(f'Пользователь с Email: {request.user.email} добавил в корзину товар (со страницы поиска товаров) "{item.product.title}" '
                    f'размер: {item.size} цвет: {item.product.color} количество: {input_quantity}')

        return redirect('cart:cart-page')

    logger.info(f'Пользователь с Email: {request.user.email} добавил в корзину товар "{item.product.title}" '
                f'размер: {item.size} цвет: {item.product.color} количество: {input_quantity}')

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
@require_POST
def add_to_cart_ajax(request):
    data = json.loads(request.body)
    product_id = data['productId']
    item_size = data['itemSize']
    item_count = int(data['itemCount'])

    product = get_object_or_404(Product, id=product_id)
    item = product.items.filter(size=item_size)[0]

    if item.item_count > 0:
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
        )
        order_qs = Order.objects.filter(user=request.user, is_active=True, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.order_items.filter(item=item).exists():
                order_item.quantity += item_count
                order_item.save()
            else:
                order_item.quantity = item_count
                order_item.save()
                order.order_items.add(order_item)
        else:
            order = Order.objects.create(user=request.user)
            order_item.quantity = item_count
            order_item.save()
            order.order_items.add(order_item)

        logger.info(f'Пользователь с Email: {request.user.email} добавил в корзину с помощью ajax запроса товар "{item.product.title}" '
                    f'размер: {item.size} цвет: {item.product.color} количество: {item_count}')

        return JsonResponse('Item added to cart', safe=False)
    else:

        logger.warning(f'Пользователь с Email: {request.user.email} пытался добавить в корзину с помощью ajax запроса '
                       f'товар "{item.product.title}",которого нет в наличии, размер: {item.size} цвет: {item.product.color} количество: {item_count}')

        return JsonResponse('Not enough items for this size', safe=False)


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
    # optimization
    order_item_qs = OrderItem.objects.select_related('item')

    order_qs = Order.objects.filter(user=request.user, is_active=True, ordered=False)\
        .prefetch_related(Prefetch('order_items', queryset=order_item_qs))

    if order_qs.exists():
        if order_qs[0].order_items.all():
            if is_enough_items(order_qs[0]):
                return render(request, 'cart/checkout_page.html')
            else:

                logger.warning(f'Пользователь с Email: {request.user.email} пытался перейти в checkout, при нехватке товаров для оформления заказа')

                return render(request, 'cart/sold_out.html')
        else:

            logger.warning(f'Пользователь с Email: {request.user.email} пытался перейти в checkout, при отсутствии товаров в заказе')

            return render(request, 'cart/empty_order.html')
    else:

        logger.warning(f'Пользователь с Email: {request.user.email} пытался перейти в checkout, при отсутствии заказа')

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

        # оповещение администратора
        send_messages_to_admin.delay(request.user.email, order.id)

        # оповещение клиента
        send_messages_to_client.delay(order.id)

        logger.info(f'Пользователь с Email: {request.user.email} оформил заказ номер {order.id} состав заказа: '
                    f'{[(order_item.item.product.title, order_item.item.product.color, order_item.item.size, order_item.quantity) for order_item in order.order_items.all()]}')

        return redirect('cart:order-complete-page', uuid=order.id)
    else:

        logger.warning(f'Пользователь с Email: {request.user.email} пытался перейти в order_complete_page, '
                       f'при нехватке товаров для оформления заказа')

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
    # optimization
    item_qs = Item.objects.select_related('product')
    order_items_qs = OrderItem.objects.prefetch_related(Prefetch('item', queryset=item_qs))

    completed_order = Order.objects.prefetch_related(Prefetch('order_items', queryset=order_items_qs)).filter(id=uuid)[0]
    return render(request, 'cart/order_complete.html', context={'completed_order': completed_order})


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
    send_messages_to_admin.delay(request.user.email, order.id, canceled=True)

    # оповещение клиента
    send_messages_to_client.delay(order.id, canceled=True)

    logger.info(f'Пользователь с Email: {request.user.email} отменил заказ номер {order.id} состав заказа: '
                f'{[(o_i.item.product.title, o_i.item.product.color, o_i.item.size, o_i.quantity) for o_i in order.order_items.all()]}')

    return redirect('users:profile-orders-page')


@login_required
def cancel_order_confirm(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'users/cancel_order_confirm.html', {'order': order})


