"""
Модуль с Celery-задачами для транзакций
"""
import os
import csv
import logging
from typing import Optional
from datetime import datetime
from django.conf import settings
from celery import shared_task
from services.date_operations import transform_date
from services.email import send_report_via_email
from .models import Transaction, ReportsResult

logger = logging.getLogger(__name__)


@shared_task  # type: ignore
def generate_transaction_report(user_id: int, start_date: Optional[str] = None,
                                end_date: Optional[str] = None, send_email: bool = False) -> str:
    """
    Фильтрация транзакций по дате и пользователю
    Аргументы:
        user_id(int): id пользователя
        start_date(str): дата начала в формате 'YYYY-MM-DD'
        end_date(str): дата завершения в формате 'YYYY-MM-DD'
    Возвращает:
        str - путь к файлу
    """
    task = ReportsResult.objects.create(user_id=user_id, task_id=generate_transaction_report.request.id,
                                        status='in_progress', send_email=send_email)
    try:
        # Фильтрация транзакций
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

        if send_email:
            # Формирование содержимого отчета для email
            report_content = [['Имя', 'Фамилия', 'Email', 'Сумма', 'Тип транзакции', 'Категория', 'Дата']]
            for transaction in transactions:
                user = transaction.user
                report_content.append([
                    user.first_name,
                    user.last_name,
                    user.email,
                    transaction.amount,
                    transaction.get_transaction_type_display_custom(),
                    transaction.category,
                    transaction.date_transaction
                ])

            # Отправка отчета на email
            send_report_via_email(report_content, first_transaction.user.email)

            task.report = None
            task.status = 'completed'
        else:
            # Сохранение отчета в CSV файл

            filename = f"report{user_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
            folder_path = os.path.join(settings.MEDIA_ROOT, 'reports')

            os.makedirs(folder_path, exist_ok=True)

            file_path = os.path.join(folder_path, filename)

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

            task.report = filename
            task.status = 'completed'

            return file_path
    except Exception as e:
        logger.info(f'Ошибка: {e}')
        task.status = 'error'
        task.error_message = str(e)
    finally:
        task.save()
