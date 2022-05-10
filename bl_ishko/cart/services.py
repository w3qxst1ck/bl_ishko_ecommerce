from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

ADMIN_EMAIL = 'sonya123@mail.ru'


def send_message_to_client(request, order):
    try:
        message_title = f'Заказ {order.id} bl_ishko'
        email = request.GET.get("email")
        from_email = 'test1@mail.ru'
        text = f'{request.GET.get("first-name")}, спасибо за Ваш заказ! Его номер номер {order.id}.\n\nВаш заказ на сумму {order.get_order_total_price_with_sale()} руб.:\n'
        count = 0
        for order_item in order.order_items.all():
            count += 1
            text += f'  {count}. {order_item.item.product.title} ({order_item.item.size}) - {order_item.quantity} шт.\n'
        text += f'\nВ ближайшее время по телефону {request.GET.get("phone")} с Вами свяжется администартор для уточнения зааказа.\n'
        send_mail(
            message_title,
            text,
            from_email,
            [email,]
        )
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def send_message_to_admin(admin_email=ADMIN_EMAIL):
    """Отправка сообщения администратору о заказе"""
    pass


def is_enough_items(order):
    for order_item in order.order_items.all():
        if order_item.item.item_count < order_item.quantity:
            return False
    return True
