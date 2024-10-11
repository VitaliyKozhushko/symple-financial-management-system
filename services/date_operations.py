"""
Модуль доя различных операция с датой
"""
from datetime import datetime
from django.db.models import Model


def formatted_date(obj: Model, date_field_name: str) -> str:
    """
    Возвращает дату в формате 'дд.мм.гггг' для указанного поля даты
    Args:
        obj (Model): экземпляр модели
        date_field_name (str): название поля даты, для которого нужно отформатировать значение
    Returns:
        str: Дата в формате 'дд.мм.гггг'.
    """
    date_value = getattr(obj, date_field_name)
    if isinstance(date_value, datetime):
        return date_value.strftime('%d.%m.%Y')
    return ''
