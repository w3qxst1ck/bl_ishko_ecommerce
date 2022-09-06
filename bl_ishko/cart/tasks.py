from .models import Order
from .services import send_message_to_client, send_message_to_admin, changed_paid_status_message
from bl_ishko.celery import app


@app.task
def send_messages_to_client(order_id, canceled=None):
    order = Order.objects.get(id=order_id)
    send_message_to_client(order, canceled)
    return 'Message to client - Done'


@app.task
def send_messages_to_admin(client_login_email, order_id, canceled=None):
    order = Order.objects.get(id=order_id)
    send_message_to_admin(client_login_email, order, canceled)
    return 'Message to admin - Done'


@app.task
def send_message_to_client_changed_paid_status(order_id):
    order = Order.objects.get(id=order_id)
    changed_paid_status_message(order)
    return 'Changed paid status message to client - Done'

