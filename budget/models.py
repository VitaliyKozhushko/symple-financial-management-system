from django.db import models
from users.models import User
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets', verbose_name='Пользователь')
    start_date = models.DateTimeField(verbose_name='Дата начала')
    end_date = models.DateTimeField(verbose_name='Дата завершения')
    budget = JSONField(default=dict, verbose_name='Бюджет')

    class Meta:
        db_table = 'budgets'
        verbose_name = 'Бюджет'
        verbose_name_plural = 'Бюджеты'

    def __str__(self):
        return f'{self.user.email} ({self.start_date} - {self.end_date})'

    def clean(self):
        """
        Проверка дат
        """
        if self.end_date <= self.start_date:
            raise ValidationError({'end_date': "Дата окончания бюджета должна быть позже даты начала."})

        last_budget = Budget.objects.filter(user=self.user).order_by('-end_date').first()
        if last_budget and self.start_date <= last_budget.end_date:
            raise ValidationError(
                {'start_date': "Дата начала бюджета должна следовать за датой завершения предыдущего бюджета."})
