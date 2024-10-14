"""
Модуль Celery-задач для транзакций
"""
import os
import logging
from typing import (cast,
                    Optional)
from datetime import datetime
from django.conf import settings
from celery import shared_task
from services.date_operations import transform_date
from services.report import send_report_email, save_csv
from .models import Transaction, ReportsResult

logger = logging.getLogger(__name__)


@shared_task  # type: ignore
def generate_transaction_report(user_id: int, start_date: Optional[str] = None,
                                end_date: Optional[str] = None,
                                send_email: bool = False) -> Optional[str]:
    """
    Фильтрация транзакций по дате и пользователю
    Аргументы:
        user_id(int): id пользователя
        start_date(str): дата начала в формате 'YYYY-MM-DD'
        end_date(str): дата завершения в формате 'YYYY-MM-DD'
    Возвращает:
        str - путь к файлу
    """
    task = ReportsResult.objects.create(user_id=user_id,
                                        task_id=generate_transaction_report.request.id,
                                        status='in_progress',
                                        send_email=send_email)
    try:
        # Фильтрация транзакций
        transactions = Transaction.objects.filter(user_id=user_id)

        if start_date and end_date:
            start_date_time, end_date_time = transform_date(start_date, end_date)
            transactions = transactions.filter(date_transaction__range=[start_date_time,
                                                                        end_date_time])

        # Путь для сохранения отчета
        first_transaction = cast(Transaction, transactions.first())
        user_name = f'_{first_transaction.user.first_name}_{first_transaction.user.last_name}'

        filename = f"report{user_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        folder_path = os.path.join(settings.MEDIA_ROOT, 'reports')

        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, filename)

        if send_email:
            send_report_email(transactions, first_transaction.user.email)
        else:
            save_csv(file_path, transactions)

        task.report = filename if not send_email else None
        task.status = 'completed'

        return file_path if not send_email else None
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.exception('Ошибка: %s', e)
        task.status = 'error'
        task.error_message = str(e)
        return None
    finally:
        task.save()
