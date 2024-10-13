"""
Модуль моделей приложения fin_transactions для хранения информации о транзакциях в БД
"""
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class Transaction(models.Model):
    """
    Модель транзакции

    Атрибуты:
        INCOME (str): константа типа транзакции "Доход"
        EXPENSE (str): константа типа транзакции "Расход"
        TRANSACTION_TYPE_CHOICES (list[tuple[str, str]]): список кортежей с выбором типа транзакции
            - INCOME ('income'): Доход
            - EXPENSE ('expense'): Расход

    Поля:
        user (ForeignKey): ссылка на пользователя, к которому относится транзакция
        amount (DecimalField): сумма транзакции. Должна быть положительным числом
        transaction_type (CharField): тип транзакции, выбор из контанты TRANSACTION_TYPE_CHOICES
        category (CharField): категория транзакции
        date_transaction (DateTimeField): дата создания транзакции. Устанавливается автоматически
        date_modified (DateTimeField): дата изменения транзакции. Обновляется автоматически
    """
    INCOME: str = 'income'
    EXPENSE: str = 'expense'

    TRANSACTION_TYPE_CHOICES: list[tuple[str, str]] = [
        (INCOME, 'Доход'),
        (EXPENSE, 'Расход'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='transactions', verbose_name='Пользователь')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма')
    transaction_type = models.CharField(max_length=7,
                                        choices=TRANSACTION_TYPE_CHOICES,
                                        verbose_name='Тип транзакции')
    category = models.CharField(max_length=100, verbose_name='Категория')
    date_transaction = models.DateTimeField(verbose_name='Дата транзакции')
    date_modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Уст. название таблицы в БД, человекочитаемое название модели
        """
        db_table = 'transactions'
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def clean(self) -> None:
        """
        Проверка на положительное значение
        """
        if self.amount <= 0:
            raise ValidationError({'amount': "Сумма транзакции должна быть больше нуля"})

    def get_transaction_type_display_custom(self) -> str:
        """Возвращает человекочитаемое название типа транзакции."""
        for value, display in self.TRANSACTION_TYPE_CHOICES:
            if self.transaction_type == value:
                return display
        return self.transaction_type

    def __str__(self) -> str:
        """
        Возвращает строковое представление транзакции: тип транзакции - сумма категория.
        """
        transaction_display = self.get_transaction_type_display_custom()
        return f"{transaction_display} - {self.amount} ({self.category})"


class ReportsResult(models.Model):
    """
        Модель Celery задач

        Атрибуты:
            STATUS_CHOICES (list[tuple[str, str]]): список статусов задач
                -('in_progress', 'In Progress') - в прогрессе
                - ('completed', 'Completed') - выполнено
                - ('error', 'Error') - ошибка

        Поля:
            user (ForeignKey): ссылка на пользователя, к которому относится задача
            task_id (CharField): id Celery задачи
            report (CharField): путь к файлу с отчетом
            send_email (BooleanField): отправка отчета на email либо сохранение в БД
            status (CharField): статус выполнения Celery задачи
            error_message (TextField): Сообщение об ошибке при наличии
            created_at (DateField): дата создания. Устанавливается автоматически
        """
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('error', 'Error'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='reports_result', verbose_name='Пользователь')
    task_id = models.CharField(max_length=255, verbose_name='Celery id')
    report = models.CharField(max_length=255, blank=True, null=True, verbose_name='Путь к отчету')
    send_email = models.BooleanField(default=False, verbose_name='Отправить на email')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='in_progress', verbose_name='Статус отчета')
    error_message = models.TextField(blank=True, null=True, verbose_name='Ошибка')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    objects = models.Manager()

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Уст. название таблицы в БД, человекочитаемое название модели
        """
        db_table = 'reports_result'
        verbose_name = 'Отчет по пользователю'
        verbose_name_plural = 'Отчеты по пользователю'

    def __str__(self) -> str:
        """
        Возвращает строковое представление Celery задачи: id задачи и пользователь, к которому
        относится данная задача.
        """
        return f"Task {self.task_id} for user {self.user}"
