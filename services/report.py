""""
Модуль для работы с отчетом
"""
import logging
import csv
from smtplib import SMTPException
from django.conf import settings
from django.core.mail import (EmailMessage,
                              BadHeaderError)
from django.db.models import QuerySet
from fin_transactions.models import Transaction

logger = logging.getLogger(__name__)


def send_report_email(transactions: QuerySet[Transaction], email_to: str) -> None:
    """Отправка CSV отчета на email"""
    try:
        report_content = [['Имя', 'Фамилия', 'Email', 'Сумма',
                           'Тип транзакции', 'Категория', 'Дата']]
        for transaction in transactions:
            user = transaction.user
            report_content.append([
                user.first_name,
                user.last_name,
                user.email,
                str(transaction.amount),
                transaction.get_transaction_type_display_custom(),
                transaction.category,
                transaction.date_transaction.strftime('%Y-%m-%d')
            ])
        email = EmailMessage(
            subject='Ваш отчет по транзакциям',
            body='Отчет по вашим транзакциям прикреплен к этому письму.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email_to]
        )
        csv_content = "\n".join([",".join(map(str, row)) for row in report_content]).encode('utf-8')
        email.attach('transaction_report.csv', csv_content, 'text/csv, charset=utf-8')
        email.send()
    except BadHeaderError as e:
        logger.error('Ошибка: Некорректный заголовок email: %s', e, exc_info=True)
    except SMTPException as e:
        logger.error('Ошибка отправки email: %s', e, exc_info=True)


def save_csv(file_path: str, transactions: QuerySet[Transaction]) -> None:
    """Сохранение отчета в CSV файл"""
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Имя', 'Фамилия', 'Email', 'Сумма',
                         'Тип транзакции', 'Категория', 'Дата'])

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
