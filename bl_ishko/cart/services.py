from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
import os

from django.template.loader import get_template
from loguru import logger

from cart.models import Order

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

        logger.info(f'Отправлено письмо клиенту на Email: {order.info.email} при оформлении заказа номер {order.id}')
    except BadHeaderError:
        logger.info(f'Не получилось отправить письмо клиенту на Email: {order.info.email} при оформлении заказа номер {order.id}')
        return HttpResponse('Invalid header found.')


def send_message_to_admin(client_login_email, order, canceled=None):
    """Отправка сообщения администратору о заказе"""
    try:
        message_title = f'Заказ {order.id} bl_ishko, {order.user.email}'
        email = ADMIN_EMAIL
        from_email = os.getenv('EMAIL_HOST_USER')

        context = {'user_email': client_login_email,
                   'order': order}
        if canceled:
            html_message = get_template('emails/admin_canceled_order.html').render(context)
        else:
            html_message = get_template('emails/admin_create_order.html').render(context)

        text = ''
        send_mail(
            message_title,
            text,
            from_email,
            [email],
            html_message=html_message,
        )
        logger.info(f'Отправлено письмо администратору на Email: {from_email} при оформлении заказа клиентом ({order.info.email}) номер {order.id}')
    except BadHeaderError:
        logger.info(f'Не получилось отправить письмо администратору при оформлении заказа клиентом ({order.info.email}) номер {order.id}')
        return HttpResponse('Invalid header found.')


def is_enough_items(order):
    for order_item in order.order_items.all():
        if order_item.item.item_count < order_item.quantity:
            return False
    return True
