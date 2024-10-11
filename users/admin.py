"""
Модуль настройки интерфейса администратора Django для управления моделью User.
"""
from django.contrib import admin
from services.date_operations import formatted_date
from .models import User


class UserAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """
    Класс настройки админ-панели Django для модели User.
    """
    list_display = (
        'id', 'first_name', 'last_name', 'email', 'formatted_date_joined')

    def formatted_date_joined(self, obj: User) -> str:
        """Использует вспомогательную функцию для форматирования даты регистрации."""
        return formatted_date(obj, 'date_joined')

    formatted_date_joined.short_description = 'Дата регистрации'  # type: ignore
    formatted_date_joined.admin_order_field = 'date_joined'  # type: ignore


admin.site.register(User, UserAdmin)
