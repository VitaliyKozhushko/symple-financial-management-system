"""
Модуль для работы с email
"""
import logging
from typing import Optional
from smtplib import SMTPException
from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError

logger = logging.getLogger(__name__)


def send_email(subject: str, body: str, from_email: str, recipient_list: list[str],
               file_content: Optional[list[list[str]]] = None) -> None:
    """
    Функция для отправки email

    :param subject: Тема email
    :param body: содержмое email
    :param from_email: email отправителя
    :param recipient_list: список email получателей
    :param file_content: содержимое файла для отправки в виде списка
    """
    email = EmailMessage(subject, body, from_email, recipient_list)
    if file_content:
        email.attach('transactions_report.csv', add_file(file_content), 'text/csv, charset=utf-8')
    try:
        email.send()
    except BadHeaderError as e:
        logger.error('Ошибка: Некорректный заголовок email: %s', e, exc_info=True)
    except SMTPException as e:
        logger.error('Ошибка отправки email: %s', e, exc_info=True)


def add_file(file_content: list[list[str]]) -> bytes:
    """
    Функция для преобразования данных в строку из списка для добавления в CSV
    :param file_content: содержимое файла для отправки
    """
    return ('\n'.join([','.join(map(str, row)) for row in file_content]) + '\n').encode('utf-8')
