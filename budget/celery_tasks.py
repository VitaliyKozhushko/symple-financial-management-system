import logging
from smtplib import SMTPException
from celery import shared_task
from django.conf import settings
from django.core.mail import (EmailMessage,
                              BadHeaderError)
from django.utils import timezone
from django.db.models import Sum
from fin_transactions.models import Transaction
from .models import Budget

logger = logging.getLogger(__name__)


@shared_task
def check_budget_limit(budget_id):
    budget = Budget.objects.get(id=budget_id)

    for transaction_type in ['income', 'expense']:
        if transaction_type in budget.budget:
            for category, data in budget.budget[transaction_type].items():
                total_actual = Transaction.objects.filter(
                    user=budget.user,
                    category=category,
                    transaction_type=transaction_type,
                    date_transaction__range=[budget.start_date, budget.end_date]
                ).aggregate(Sum('amount'))['amount__sum'] or 0

                # Обновляем фактическое значение
                data['actual'] = total_actual

                # Проверяем, нужно ли отправить оповещение
                if total_actual >= 0.9 * data['forecast'] and not data['is_notified']:
                    send_budget_notification(budget, transaction_type, category, data['forecast'], total_actual)
                    data['is_notified'] = True
                    data['date_notified'] = timezone.now().date().isoformat()

    # Сохраняем обновленный бюджет
    budget.save()


def send_budget_notification(budget, transaction_type, category, forecast, actual):
    try:
        email = EmailMessage(
            subject='Предупреждение о бюджете',
            body=(
                f"Ваш лимит по категории '{category}' ({transaction_type}) "
                f"приблизился к 90%. Прогноз: {forecast}, Фактически: {actual}."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[budget.user.email]
        )
        email.send()
    except BadHeaderError as e:
        logger.error('Ошибка: Некорректный заголовок email: %s', e, exc_info=True)
    except SMTPException as e:
        logger.error('Ошибка отправки email: %s', e, exc_info=True)
