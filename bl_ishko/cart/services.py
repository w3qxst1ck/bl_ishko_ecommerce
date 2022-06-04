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


def send_message_to_admin(client_login_email, order, canceled=None):
    """Отправка сообщения администратору о заказе"""
    try:
        message_title = f'Заказ {order.id} bl_ishko, {order.user.email}'
        email = os.getenv('ADMIN_EMAIL')
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
            from_email,
            text,
            [email],
            html_message=html_message,
        )
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def is_enough_items(order):
    for order_item in order.order_items.all():
        if order_item.item.item_count < order_item.quantity:
            return False
    return True
