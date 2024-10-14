from django.db import models
from users.models import User
import logging

logger = logging.getLogger(__name__)


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets', verbose_name='Пользователь')
    start_date = models.DateTimeField(verbose_name='Дата начала')
    end_date = models.DateTimeField(verbose_name='Дата завершения')
    budget = models.JSONField(default=dict, verbose_name='Бюджет')

    class Meta:
        db_table = 'budgets'
        verbose_name = 'Бюджет'
        verbose_name_plural = 'Бюджеты'

    def __str__(self) -> str:
        return f'{self.user.email} ({self.start_date} - {self.end_date})'
