from bl_ishko.celery import app
from shop.services import send_mail_from_contact


@app.task
def send_messages_from_contact_task(name, email, topic, message_text):
    send_mail_from_contact(name, email, topic, message_text)
    return 'Send message from contact page - Done'

