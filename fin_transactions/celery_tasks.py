"""
Модуль с Celery-задачами для транзакций
"""
import csv
from typing import Optional
from datetime import datetime
from django.conf import settings
from celery import shared_task
from services.date_operations import transform_date
from .models import Transaction


@shared_task  # type: ignore
def generate_transaction_report(user_id: int, start_date: Optional[str] = None,
                                end_date: Optional[str] = None) -> str:
    """
    Фильтрация транзакций по дате и пользователю
    Аргументы:
        user_id(int): id пользователя
        start_date(str): дата начала в формате 'YYYY-MM-DD'
        end_date(str): дата завершения в формате 'YYYY-MM-DD'
    Возвращает:
        str - путь к файлу
    """
    transactions = Transaction.objects.filter(user_id=user_id)

    if start_date and end_date:
        start_date_time, end_date_time = transform_date(start_date, end_date)
        transactions = transactions.filter(date_transaction__range=[start_date_time, end_date_time])

    # Путь для сохранения отчета
    first_transaction = transactions.first()
    if not first_transaction:
        user_name = ''
    else:
        user_name = f'_{first_transaction.user.first_name}_{first_transaction.user.last_name}'

    filename = f"report{user_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    file_path = f"{settings.STATIC_ROOT}{filename}"

    # Сохранение отчета в CSV файл
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Имя', 'Фамилия', 'Email', 'Сумма', 'Тип транзакции', 'Категория', 'Дата'])

        for transaction in transactions:
            user = transaction.user
            writer.writerow([
                user.first_name,
                user.last_name,
                user.email,
                transaction.amount,
                transaction.get_transaction_type_display_custom(),
                transaction.category,
                transaction.date_transaction
            ])

    return file_path
