from .models import Order
from .services import send_message_to_client, send_message_to_admin
from bl_ishko.celery import app


@app.task
def send_messages(request, order_id, message_to, canceled=None):
    order = Order.objects.get(id=order_id)
    if message_to == 'admin':
        send_message_to_admin(request, order, canceled)
    else:
        send_message_to_client(order, canceled)


@app.task
def test_func(s):
    print(s)
