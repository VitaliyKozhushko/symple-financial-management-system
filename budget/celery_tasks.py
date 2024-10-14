"""
Модуль Celery-задач для бюджета
"""
import logging
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum
from fin_transactions.models import Transaction
from services.email import send_email
from .models import Budget

logger = logging.getLogger(__name__)


@shared_task  # type: ignore
def check_budget_limit(budget_id: int) -> None:
    """
    Проверяем налие бюджета по категории и выполнение бюджета до опр. уровня
    :param budget_id: id бюджета
    """
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

                data['actual'] = float(total_actual)

                budget_amounts = {
                    'forecast': data['forecast'],
                    'actual': total_actual
                }
                # Проверяем, нужно ли отправить оповещение для пустого бюджета
                if data['forecast'] == 0:
                    send_budget_notification(budget, transaction_type,
                                             category, budget_amounts,
                                             'zero_budget')

                # Проверяем, нужно ли отправить оповещение при приближении к лимиту бюджета
                if (total_actual >= 0.9 * data['forecast'] and
                        data['forecast'] > 0 and
                        not data['is_notified']):
                    send_budget_notification(budget, transaction_type,
                                             category, budget_amounts,
                                             'limit_budget')
                    data['is_notified'] = True
                    data['date_notified'] = timezone.now().date().isoformat()

    budget.save()


def send_budget_notification(
    budget: Budget,
    transaction_type: str,
    category: str,
    budget_amounts: dict[str, float],
    type_notify: str
) -> None:
    """
    Отправляет уведомление пользователю о подходе к лимиту бюджета либо отсутствии бюджета

    :param budget: экземпляр бюджета
    :param transaction_type: тип транзакции ('income' или 'expense')
    :param category: категория транзакции
    :param budget_amounts: словарь с прогнозируемой суммой бюджета и фактической
    :param type_notify: тип уведомления ('zero_budget' или 'limit_budget')
    """
    subject_email = 'Предупреждение о бюджете' if type_notify == 'limit_budget' \
        else 'Предупреждение о незаполненом бюджете'
    body_email = (
        f"Ваш лимит по категории '{category}' ({transaction_type}) "
        f"приблизился к 90%. Прогноз: {budget_amounts['forecast']}, "
        f"Фактически: {budget_amounts['actual']}."
    ) if type_notify == 'limit_budget' \
        else f"Необходимо установить бюджет по категории '{category}' ({transaction_type})"

    send_email(subject_email, body_email, settings.DEFAULT_FROM_EMAIL, [budget.user.email])
