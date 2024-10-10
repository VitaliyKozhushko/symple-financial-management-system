"""
Модуль настройки интерфейса администратора для управления моделью Transaction.
"""
from datetime import datetime
from django.contrib import admin
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """
    Настройка админ-панели Django для модели Transaction.
    """
    list_display = ('id', 'user', 'user_id_display', 'amount',
                    'transaction_type', 'category', 'formatted_date_transaction')

    def formatted_date_transaction(self, obj: Transaction) -> str:
        """
        Возвращает дату транзакции в формате 'дд.мм.гггг'.
        Args:
            obj (Transaction): Экземпляр модели Transaction.
        Returns:
            str: Дата транзакции в формате 'дд.мм.гггг'.
        """
        date_transaction: datetime = obj.date_transaction
        return date_transaction.strftime('%d.%m.%Y')

    formatted_date_transaction.short_description = 'Дата транзакции'  # type: ignore
    formatted_date_transaction.admin_order_field = 'date'  # type: ignore

    def user_id_display(self, obj: Transaction) -> int:
        """
        Возвращает id пользователя.
        Args:
            obj (Transaction): Экземпляр модели Transaction.
        Returns:
            int: id пользователя.
        """
        return obj.user.id

    user_id_display.short_description = 'ID пользователя'  # type: ignore


admin.site.register(Transaction, TransactionAdmin)
