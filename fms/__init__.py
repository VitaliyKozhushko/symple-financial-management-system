"""
Модуль инициализации Celery приложения для использования в проекте Django.
"""

from .celery import app as celery_app

__all__ = ('celery_app',)
