from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

# Задаем переменную окружения, содержащую название файла настроек нашего проекта.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bl_ishko.settings')

app = Celery('bl_ishko')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
