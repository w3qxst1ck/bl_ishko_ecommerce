from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
import os

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')


def send_message_to_client(order, canceled=None):
    try:
        message_title = f'Заказ {order.id} bl_ishko'
        email = order.info.email
        from_email = 'test1@mail.ru'

        if canceled:
            text = client_message_text_canceled_order(order)
        else:
            text = client_message_text_created_order(order)

        send_mail(
            message_title,
            text,
            from_email,
            [email,]
        )
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def client_message_text_created_order(order):
    """Сообщение для клиента об оформлении нового заказа."""
    text = f'{order.info.first_name}, спасибо за Ваш заказ! Его номер номер № {order.id}.\n\nВаш заказ на сумму {order.get_order_total_price_with_sale()} руб.:\n'
    count = 0
    for order_item in order.order_items.all():
        count += 1
        text += f'  {count}. {order_item.item.product.title} ({order_item.item.size}) - {order_item.quantity} шт.\n'
    text += f'\nВ ближайшее время по телефону {order.info.phone} с Вами свяжется администартор для уточнения зааказа.\n'
    return text


def client_message_text_canceled_order(order):
    text = f'{order.info.first_name}, вы отменили заказ № {order.id}.\nЕго состав:\n'
    count = 0
    for order_item in order.order_items.all():
        count += 1
        text += f'  {count}. {order_item.item.product.title} ({order_item.item.size}) - {order_item.quantity} шт.\n'
    if order.paid:
        text += f'С Вами свяжется администратор для возврата средств по телефону {order.info.phone}, сумма к возврату - {order.get_order_total_price_with_sale()} + цена за доставку.\nВы также можете связаться с администратором по телефону 8(800)555-35-35 для уточнения информации.'
    else:
        text += f'Если у Вас остались какие то вопросы, вы можете связаться с администратором по номеру 8(800)555-35-35 или написать в поддержу на сайте в разделе "Контакты".'
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
    text = f'Пользователь {request.user.email} ({order.info.first_name} {order.info.last_name}) оформил заказ № {order.id}.\nСостав заказа:\n'
    count = 0
    for order_item in order.order_items.all():
        count += 1
        text += f'{count}. {order_item.item.product.title} ({order_item.item.size}) - {order_item.quantity} шт.\n'
    if order.info.payment_method == 'CASH':
        payment_method = 'Наличными'
    else:
        payment_method = 'Картой'
    text += f'Сумма заказа - {order.get_order_total_price_with_sale()} руб. (без скидки - {order.get_order_total_price()} руб.) + доставка 500 руб.\nМетод оплаты: \"{payment_method}\".\n'
    text += f'Заказ оформлен на адресс:\nСтрана: \"Россия\",\nРегион: \"{order.info.region}\",\nГород (населенный пункт): \"{order.info.city}\",\nАдрес: \"{order.info.address}\".\n'
    text += f'Телефон для связи: {order.info.phone}, email: {order.info.email}.'
    return text


def admin_message_text_canceled_order(request, order):
    text = f'Пользователь {request.user.email} ({order.info.first_name} {order.info.last_name}) отменил заказ № {order.id}.\n'
    text += f'Телефон для связи с клиентом {order.info.phone}.\n'
    if order.paid:
        text += f'Сумма к возврату клиенту - {order.get_order_total_price_with_sale()} руб. + цена за доставку (если доставка оплачена).\n'
    else:
        text += f'Заказ не был оплачен. Сумма к возврату - 0 руб.\n'
    text += 'Состав заказа:\n'
    count = 0
    for order_item in order.order_items.all():
        count += 1
        text += f'{count}. {order_item.item.product.title} ({order_item.item.size}) - {order_item.quantity} шт.\n'
    text += f'Общая сумма заказа - {order.get_order_total_price_with_sale()} руб.'
    return text


def is_enough_items(order):
    for order_item in order.order_items.all():
        if order_item.item.item_count < order_item.quantity:
            return False
    return True
