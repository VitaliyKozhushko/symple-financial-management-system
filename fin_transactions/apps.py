"""
Модуль конфига приложения fin_transactions
"""
from django.apps import AppConfig


class FinTransactionsConfig(AppConfig):
    """
    Конфиг для приложения fin_transactions
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fin_transactions'
    verbose_name = 'Транзакции'
