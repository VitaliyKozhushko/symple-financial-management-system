"""
Инициализирует и настраивает приложение Celery для проекта Django,
загружая настройки из `settings.py`.
Автоматически обнаруживает и регистрирует задачи из всех установленных приложений.
"""
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fms.settings')

app = Celery('fms')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
