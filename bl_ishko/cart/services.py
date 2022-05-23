from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

ADMIN_EMAIL = 'bl.ishko@yandex.ru'


def send_message_to_client(request, order):
    try:
        message_title = f'Заказ {order.id} bl_ishko'
        email = request.GET.get("email")
        from_email = 'test1@mail.ru'
        text = get_client_message_text(request, order)
        send_mail(
            message_title,
            text,
            from_email,
            [email,]
        )
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def get_client_message_text(request, order):
    text = f'{request.GET.get("first-name")}, спасибо за Ваш заказ! Его номер номер № {order.id}.\n\nВаш заказ на сумму {order.get_order_total_price_with_sale()} руб.:\n'
    count = 0
    for order_item in order.order_items.all():
        count += 1
        text += f'  {count}. {order_item.item.product.title} ({order_item.item.size}) - {order_item.quantity} шт.\n'
    text += f'\nВ ближайшее время по телефону {request.GET.get("phone")} с Вами свяжется администартор для уточнения зааказа.\n'
    return text


def send_message_to_admin_created_order(request, order, admin_email=ADMIN_EMAIL):
    """Отправка сообщения администратору о заказе"""
    try:
        message_title = f'Заказ {order.id} bl_ishko, {order.user.email}'
        email = admin_email
        from_email = 'test1@mail.ru'

        text = get_admin_message_text(request, order)

        send_mail(
            message_title,
            text,
            from_email,
            [email, ]
        )
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def get_admin_message_text(request, order):
    text = f'Пользователь {order.user.email} ({request.GET.get("first-name")} {request.GET.get("last-name")}) оформил заказ № {order.id}.\nСостав заказа:\n'
    count = 0
    for order_item in order.order_items.all():
        count += 1
        text += f'{count}. {order_item.item.product.title} ({order_item.item.size}) - {order_item.quantity} шт.\n'
    text += f'Сумма заказа - {order.get_order_total_price_with_sale()} руб. (без скидки - {order.get_order_total_price()} руб.) + доставка 500 руб.\nМетод оплаты: \"{order.payment_method}\".\n'
    text += f'Заказ оформлен на адресс:\nСтрана: \"Россия\",\nРегион: \"{request.GET.get("region")}\",\nГород (населенный пункт): \"{request.GET.get("city")}\",\nАдрес: \"{request.GET.get("address")}\".\n'
    text += f'Телефон для связи: {request.GET.get("phone")}, email: {request.GET.get("email")}.'
    return text


def send_message_to_admin_canceled_order():
    pass


def is_enough_items(order):
    for order_item in order.order_items.all():
        if order_item.item.item_count < order_item.quantity:
            return False
    return True
