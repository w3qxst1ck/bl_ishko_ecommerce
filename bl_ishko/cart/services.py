from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
import os

from django.template.loader import get_template

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')


def send_message_to_client(order, canceled=None):
    try:
        message_title = f'Заказ {order.id} bl_ishko'
        email = order.info.email
        from_email = os.getenv('EMAIL_HOST_USER')
        context = {'order': order}
        if canceled:
            html_message = get_template('emails/client_canceled_order.html').render(context)
        else:
            html_message = get_template('emails/client_create_order.html').render(context)

        text = ''
        send_mail(
            message_title,
            text,
            from_email,
            [email],
            html_message=html_message
        )
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def client_message_text_created_order(order):
    """Сообщение для клиента об оформлении нового заказа."""
    text = f'{order.info.first_name}, спасибо за Ваш заказ! Его номер номер № {order.id}.\n\nВаш заказ:\n'
    count = 0
    for order_item in order.order_items.all():
        count += 1
        text += f'  {count}. {order_item.item.product.title} ({order_item.item.size}) - {order_item.quantity} шт. {order_item.item_total_with_sale()} руб.\n'
    text += f'Общая сумма заказа {order.get_order_total_price_with_sale()} руб.\n'
    text += f'\nВ ближайшее время по телефону {order.info.phone} с Вами свяжется администартор для уточнения зааказа и способа доставки.\n'
    return text


def client_message_text_canceled_order(order):
    text = f'{order.info.first_name}, вы отменили заказ № {order.id}.\nЕго состав:\n'
    count = 0
    for order_item in order.order_items.all():
        count += 1
        text += f'  {count}. {order_item.item.product.title} ({order_item.item.size}) - {order_item.quantity} шт. {order_item.item_total_with_sale()} руб.\n'
    if order.paid:
        sum_with_delivery = order.get_order_total_price_with_sale() + order.info.delivery_price
        text += f'С Вами свяжется администратор для возврата средств по телефону {order.info.phone}, сумма к возврату - {sum_with_delivery} руб. (сумма заказа - {order.get_order_total_price_with_sale()} руб., цена доставки - {order.info.delivery_price} руб.)\nВы также можете связаться с администратором по телефону 8(800)555-35-35 для уточнения информации.'
    else:
        text += f'Если у Вас остались какие то вопросы, вы можете связаться с администратором по номеру 8(800)555-35-35 или написать в поддержу на сайте в разделе "Контакты".'
    return text


def send_message_to_admin(request, order, admin_email=ADMIN_EMAIL, canceled=None):
    """Отправка сообщения администратору о заказе"""
    try:
        message_title = f'Заказ {order.id} bl_ishko, {order.user.email}'
        email = admin_email
        from_email = os.getenv('EMAIL_HOST_USER')
        context = {'user_email': request.user.email,
                   'order': order}
        if canceled:
            html_message = get_template('emails/admin_canceled_order.html').render(context)
        else:
            html_message = get_template('emails/admin_create_order.html').render(context)

        text = ''
        send_mail(
            message_title,
            from_email,
            text,
            [email, ],
            html_message=html_message,

        )
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def admin_message_text_created_order(request, order):
    """Сообщение для администратора об оформлении нового заказа."""
    text = f'Пользователь {request.user.email} ({order.info.first_name} {order.info.last_name}) оформил заказ № {order.id}.\nСостав заказа:\n'
    count = 0
    for order_item in order.order_items.all():
        count += 1
        text += f'{count}. {order_item.item.product.title} ({order_item.item.size}) - {order_item.quantity} шт. {order_item.item_total_with_sale()} руб.\n'
    if order.info.payment_method == 'CASH':
        payment_method = 'Наличными'
    else:
        payment_method = 'Картой'
    text += f'Сумма заказа - {order.get_order_total_price_with_sale()} руб. (без скидки - {order.get_order_total_price()} руб.) + цена за доставку.\n\nМетод оплаты: \"{payment_method}\".\n'
    text += f'Заказ оформлен на адресс:\nСтрана: \"Россия\",\nРегион: \"{order.info.region}\",\nГород (населенный пункт): \"{order.info.city}\",\nАдрес: \"{order.info.address}\",\n'
    text += f'Комментарий к заказу: "{order.info.order_comment}".\n'
    text += f'\nВам необходимо связаться с клиентом, для уточнения способа и суммы доставки (после внести данные в администраторской панели)\n'
    text += f'Телефон для связи: {order.info.phone}, email: {order.info.email}.'
    return text


def admin_message_text_canceled_order(request, order):
    text = f'Пользователь {request.user.email} ({order.info.first_name} {order.info.last_name}) отменил заказ № {order.id}.\n'
    text += f'Телефон для связи с клиентом {order.info.phone}.\n'
    if order.paid:
        sum_with_delivery = order.get_order_total_price_with_sale() + order.info.delivery_price
        text += f'Сумма к возврату клиенту - {sum_with_delivery} руб. (сумма заказа - {order.get_order_total_price_with_sale()} руб., цена доставки - {order.info.delivery_price} руб.)\n'
    else:
        text += f'Заказ не был оплачен. Сумма к возврату - 0 руб.\n'
    text += 'Состав заказа:\n'
    count = 0
    for order_item in order.order_items.all():
        count += 1
        text += f'{count}. {order_item.item.product.title} ({order_item.item.size}) - {order_item.quantity} шт. {order_item.item_total_with_sale()} руб.\n'
    text += f'Общая сумма заказа - {order.get_order_total_price_with_sale()} руб.'
    return text


def is_enough_items(order):
    for order_item in order.order_items.all():
        if order_item.item.item_count < order_item.quantity:
            return False
    return True
