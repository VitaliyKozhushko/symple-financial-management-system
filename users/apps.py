"""
Модуль конфигурации приложения Users для Django.
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Класс конфиг для приложения 'users'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
