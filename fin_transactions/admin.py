"""
Модуль настройки интерфейса администратора для управления моделью Transaction.
"""
from django.contrib import admin
from services.date_operations import formatted_date
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """
    Настройка админ-панели Django для модели Transaction.
    """
    list_display = ('id', 'user', 'user_id_display', 'amount',
                    'transaction_type', 'category', 'formatted_date_transaction')

    def formatted_date_transaction(self, obj: Transaction) -> str:
        """Использует вспомогательную функцию для форматирования даты транзакции."""
        return formatted_date(obj, 'date_transaction')

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
