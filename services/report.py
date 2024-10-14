""""
Модуль для работы с отчетом
"""
import logging
import csv
from django.conf import settings
from django.db.models import QuerySet
from fin_transactions.models import Transaction
from .email import send_email

logger = logging.getLogger(__name__)


def send_report_email(transactions: QuerySet[Transaction], email_to: str) -> None:
    """Отправка CSV отчета на email"""
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
    send_email('Ваш отчет по транзакциям',
               'Отчет по вашим транзакциям прикреплен к этому письму.',
               settings.DEFAULT_FROM_EMAIL, [email_to],
               report_content)


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
