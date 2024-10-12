"""
Модуль доя различных операция с датой
"""
from typing import Tuple
from datetime import datetime, timedelta
from django.db.models import Model
from django.utils import timezone


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


def transform_date(start_date_str: str, end_date_str: str) -> Tuple[datetime, datetime]:
    """
    Преобразование строк дат в объекты datetime с учетом временной зоны.

    Аргументы:
        start_date_str(str): дата начала в формате 'YYYY-MM-DD'
        end_date_str(str): дата окончания в формате 'YYYY-MM-DD'
    Возвращает:
        Tuple[timezone.datetime, timezone.datetime]: кортеж, содержащий два объекта datetime:
        - начало диапазона с учетом времени 00:00:00
        - конец диапазона с учетом времени 23:59:59
    """
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    transform_end_date = end_date + timedelta(days=1) - timedelta(microseconds=1)
    start_date_time = timezone.make_aware(start_date)
    end_date_time = timezone.make_aware(transform_end_date)
    return start_date_time, end_date_time
