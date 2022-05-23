from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

ADMIN_EMAIL = 'bl.ishko@yandex.ru'


def send_message_to_client(request, order, canceled=None):
    try:
        message_title = f'Заказ {order.id} bl_ishko'
        email = request.GET.get("email")
        from_email = 'test1@mail.ru'

        if canceled:
            text = client_message_text_canceled_order(request, order)
        else:
            text = client_message_text_created_order(request, order)

        send_mail(
            message_title,
            text,
            from_email,
            [email,]
        )
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def client_message_text_created_order(request, order):
    """Сообщение для клиента об оформлении нового заказа."""
    text = f'{request.GET.get("first-name")}, спасибо за Ваш заказ! Его номер номер № {order.id}.\n\nВаш заказ на сумму {order.get_order_total_price_with_sale()} руб.:\n'
    count = 0
    for order_item in order.order_items.all():
        count += 1
        text += f'  {count}. {order_item.item.product.title} ({order_item.item.size}) - {order_item.quantity} шт.\n'
    text += f'\nВ ближайшее время по телефону {request.GET.get("phone")} с Вами свяжется администартор для уточнения зааказа.\n'
    return text


def client_message_text_canceled_order(request, order):
    text = f'{order.user.first_name}, вы отменили заказ № {order.id}.\n Его состав:\n'
    count = 0
    for order_item in order.order_items.all():
        count += 1
        text += f'  {count}. {order_item.item.product.title} ({order_item.item.size}) - {order_item.quantity} шт.\n'
    text += f'Если заказ был уже оплачен, с Вами свяжется администратор для возврата средств по телефону {request.user.info.phone}.\nВы также можете связаться с администратором по телефону 8(800)555-35-35 для уточнения информации.'
    return text


def send_message_to_admin(request, order, admin_email=ADMIN_EMAIL, canceled=None):
    """Отправка сообщения администратору о заказе"""
    try:
        message_title = f'Заказ {order.id} bl_ishko, {order.user.email}'
        email = admin_email
        from_email = 'test1@mail.ru'

        if canceled:
            text = admin_message_text_canceled_order(request, order)
        else:
            text = admin_message_text_created_order(request, order)

        send_mail(
            message_title,
            text,
            from_email,
            [email, ]
        )
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def admin_message_text_created_order(request, order):
    """Сообщение для администратора об оформлении нового заказа."""
    text = f'Пользователь {order.user.email} ({request.GET.get("first-name")} {request.GET.get("last-name")}) оформил заказ № {order.id}.\nСостав заказа:\n'
    count = 0
    for order_item in order.order_items.all():
        count += 1
        text += f'{count}. {order_item.item.product.title} ({order_item.item.size}) - {order_item.quantity} шт.\n'
    text += f'Сумма заказа - {order.get_order_total_price_with_sale()} руб. (без скидки - {order.get_order_total_price()} руб.) + доставка 500 руб.\nМетод оплаты: \"{order.payment_method}\".\n'
    text += f'Заказ оформлен на адресс:\nСтрана: \"Россия\",\nРегион: \"{request.GET.get("region")}\",\nГород (населенный пункт): \"{request.GET.get("city")}\",\nАдрес: \"{request.GET.get("address")}\".\n'
    text += f'Телефон для связи: {request.GET.get("phone")}, email: {request.GET.get("email")}.'
    return text


def admin_message_text_canceled_order(request, order):
    text = f'Пользователь {request.user.email} ({request.user.first_name} {request.user.last_name}) отменил заказ № {order.id}.\n'
    text += f'Телефон для связи с клиентом {request.user.info.phone} (если заказ был оплачен, необходимо вернуть деньги клиенту).\nСостав заказа:\n'

    count = 0
    for order_item in order.order_items.all():
        count += 1
        text += f'{count}. {order_item.item.product.title} ({order_item.item.size}) - {order_item.quantity} шт.\n'

    return text


def is_enough_items(order):
    for order_item in order.order_items.all():
        if order_item.item.item_count < order_item.quantity:
            return False
    return True
