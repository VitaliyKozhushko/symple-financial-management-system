"""
Модуль моделей приложения budget для хранения информации о бюджете в БД
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Budget(models.Model):
    """
    Модель бюджета

    Поля:
        user (ForeignKey): ссылка на пользователя, к которому относится бюджет
        start_date (DateTimeField): дата начала бюджета
        end_date (DateTimeField): дата завершения бюджета
        budget (JSONField): бюджет, содержащий прогноз и фактические данные по доходам и расходам.

    Структура JSON:
    {
        "income": {
            "category_name": {
                "forecast": float,  # прогнозируемая сумма дохода для категории
                "actual": float,  # фактическая сумма дохода для категории
                "is_notified": bool,  # было ли отправлено уведомление о пересечении 90% от бюджета
                "date_notified": Optional[datetime]  # дата отправки уведомления, если отправлено
            },
            ...
        },
        "expense": {
            "category_name": {
                "forecast": float,  # прогнозируемая сумма расхода для категории
                "actual": float,  # фактическая сумма расхода для категории
                "is_notified": bool,  # было ли отправлено уведомление о пересечении 90% от бюджета
                "date_notified": Optional[datetime]  # дата отправки уведомления, если отправлено
            },
            ...
        }
    }
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='budgets', verbose_name='Пользователь')
    start_date = models.DateTimeField(verbose_name='Дата начала')
    end_date = models.DateTimeField(verbose_name='Дата завершения')
    budget = models.JSONField(default=dict, verbose_name='Бюджет')

    objects = models.Manager()

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Уст. название таблицы в БД, человекочитаемое название модели
        """
        db_table = 'budgets'
        verbose_name = 'Бюджет'
        verbose_name_plural = 'Бюджеты'

    def __str__(self) -> str:
        return f'{self.user} ({self.start_date} - {self.end_date})'
