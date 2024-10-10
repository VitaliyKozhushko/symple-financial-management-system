"""
Модуль конфигурации приложения users для Django.
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Конфиг для приложения 'users'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Пользователи'
