from django.db import models
from users.models import User
from django.core.exceptions import ValidationError


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets', verbose_name='Пользователь')
    start_date = models.DateTimeField(verbose_name='Дата начала')
    end_date = models.DateTimeField(verbose_name='Дата завершения')
    budget = models.JSONField(default=dict, verbose_name='Бюджет')

    class Meta:
        db_table = 'budgets'
        verbose_name = 'Бюджет'
        verbose_name_plural = 'Бюджеты'

    def __str__(self):
        return f'{self.user.email} ({self.start_date} - {self.end_date})'

    def clean(self):
        """
        Проверка дат и структуры бюджета
        """
        # проверка дат
        if self.end_date <= self.start_date:
            raise ValidationError({'end_date': "Дата окончания бюджета должна быть позже даты начала."})

        last_budget = Budget.objects.filter(user=self.user).order_by('-end_date').first()
        if last_budget and self.start_date <= last_budget.end_date:
            raise ValidationError(
                {'start_date': "Дата начала бюджета должна следовать за датой завершения предыдущего бюджета."})

        # Проверка структуры поля budget
        if not isinstance(self.budget, dict):
            raise ValidationError({'budget': "Бюджет должен быть в формате JSON-объекта."})

        for transaction_type in ['income', 'expense']:
            if transaction_type in self.budget:
                for category, data in self.budget[transaction_type].items():
                    if 'forecast' not in data or 'actual' not in data:
                        raise ValidationError(
                            {'budget': f"Категория {category} должна содержать 'forecast' и 'actual'."})
                    if not isinstance(data['forecast'], (int, float)) or not isinstance(data['actual'],
                                                                                        (int, float)):
                        raise ValidationError({
                                                    'budget': f"Значения 'forecast' и 'actual' в категории {category} должны быть числовыми."})
