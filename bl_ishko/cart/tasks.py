from .models import Order
from .services import send_message_to_client, send_message_to_admin
from bl_ishko.celery import app


@app.task
def send_messages_to_client(order_id, canceled=None):
    order = Order.objects.get(id=order_id)
    send_message_to_client(order, canceled)
    return 'Message to client - Done'


@app.task
def send_messages_to_admin(user_email, order_id, canceled=None):
    order = Order.objects.get(id=order_id)
    send_message_to_admin(user_email, order, canceled)
    return 'Message to admin - Done'

