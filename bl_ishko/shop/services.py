import os
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from loguru import logger

from .models import Product


def get_related_products_for_detail(product, count=6):
    id_already_in_use = []
    related_products = []

    # такие же продукты только другого цвета
    same_name_products = Product.objects.filter(Q(title=product.title) & ~Q(id=product.id)).prefetch_related('items')
    related_products.extend(same_name_products)
    id_already_in_use.extend([product.id for product in same_name_products])

    # продукты той же категории
    same_category_products = Product.objects.filter(~Q(id__in=id_already_in_use) & Q(category=product.category)).prefetch_related('items')
    related_products.extend(same_category_products)
    id_already_in_use.extend([product.id for product in same_category_products])

    related_products.remove(product)
    if len(related_products) < count:
        related_products.extend(Product.objects.filter(~Q(id__in=id_already_in_use)).prefetch_related('items').order_by('-created')[:count - len(related_products)])

    return related_products[:count]


def get_size_list(products):
    all_sizes = ['XS', 'S', 'M', 'L', 'XL']
    size_list = []
    for s in all_sizes:
        if len(products.filter(items__size=s)) > 0:
            size_list.append(s)
    return size_list


def search_products(request):
    pass


def send_mail_from_contact(name, from_email, topic, message_text, admin_email=os.getenv('ADMIN_EMAIL')):
    if topic:
        text = f'Сообщение от {name}, электронная почта {from_email}\nТема сообщения: {topic}\n' \
           f'Текст сообщения:\n' \
           f'{message_text}'
    else:
        text = f'Сообщение от {name}, электронная почта {from_email}\n' \
               f'Текст сообщения:\n' \
               f'{message_text}'
    try:
        message_title = topic if topic else 'Без темы'
        send_mail(message_title, text, os.getenv('DEFAULT_FROM_EMAIL'), [admin_email])
        logger.info(f'Отправлено письмо со страницы контактов на Email администратора: {admin_email}. '
                    f'Email для обратной свзяи {from_email}')
    except BadHeaderError:
        logger.warning(f'Не получилось отправить письмо администратору на почту {admin_email} со страницы контактов. '
                       f'Email для обратной свзяи {from_email}')
        return HttpResponse('Invalid header found.')
