"""
Модуль для настройки интерфейса администратора Django для управления моделью User.
"""
from datetime import datetime
from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """
    Класс для настройки админ-панели Django для модели User.
    """
    list_display = (
        'id', 'first_name', 'last_name', 'email', 'formatted_date_joined')

    def formatted_date_joined(self, obj: User) -> str:
        """
        Возвращает дату регистрации пользователя в формате 'дд.мм.гггг'.
        Args:
            obj (User): Экземпляр модели User.
        Returns:
            str: Дата регистрации пользователя в формате 'дд.мм.гггг'.
        """
        date_joined: datetime = obj.date_joined
        return date_joined.strftime('%d.%m.%Y')

    formatted_date_joined.short_description = 'Дата регистрации'  # type: ignore
    formatted_date_joined.admin_order_field = 'date_joined'  # type: ignore


admin.site.register(User, UserAdmin)
