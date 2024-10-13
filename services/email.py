from django.core.mail import EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_report_via_email(report_content, email_to):
    try:
        email = EmailMessage(
            subject='Ваш отчет по транзакциям',
            body='Отчет по вашим транзакциям прикреплен к этому письму.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email_to]
        )
        csv_content = "\n".join([",".join(map(str, row)) for row in report_content]).encode('utf-8')
        email.attach('transaction_report.csv', csv_content, 'text/csv, charset=utf-8')
        email.send()
    except Exception as e:
        logger.error(f'Ошибка отправки email: {e}', exc_info=True)