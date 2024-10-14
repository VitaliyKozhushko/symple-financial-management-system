"""
Модуль конфига приложения budget
"""
from django.apps import AppConfig


class BudgetConfig(AppConfig):
    """
    Конфиг для приложения budget
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'budget'
