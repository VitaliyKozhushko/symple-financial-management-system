"""
Модуль для представлений модели Transaction
"""
from typing import Any
from decimal import (Decimal,
                     InvalidOperation)
from rest_framework import (generics,
                            status)
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from services.decorators import add_bearer_security, swagger_auto_schema_with_types
from .celery_tasks import generate_transaction_report
from .models import Transaction
from .serializers import TransactionsSerializer


def validate_amount(data: dict[str, Any]) -> Decimal:
    """
        Проверяет, что сумма (amount) является числом и больше нуля.
        Возвращает значение суммы как Decimal, если проверка пройдена.

        Аргументы:
            data (dict[str, Any]): данные запроса
        Возвращает:
            Decimal: проверенное значение 'amount'
        Исключения:
            ValidationError: если сумма не является числом или меньше либо равна нулю
        """
    try:
        amount = Decimal(data.get('amount', '0'))
    except (ValueError, TypeError, InvalidOperation) as err:
        raise ValidationError({"amount": "Сумма транзакции должна быть числом."}) from err

    if amount <= 0:
        raise ValidationError({"amount": "Сумма транзакции должна быть больше нуля"})

    return amount


class TransactionListCreateView(generics.ListCreateAPIView):  # type: ignore
    """
    Получение списка транзакций и создание транзакции
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionsSerializer

    @add_bearer_security
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)

    @add_bearer_security
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        validate_amount(request.data)
        return super().post(request, *args, **kwargs)


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):  # type: ignore
    """
    Получение данных по опр. транзакции, редактирование транзакции и её удаление
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionsSerializer
    http_method_names = ['get', 'put', 'delete']

    @add_bearer_security
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)

    @add_bearer_security
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        validate_amount(request.data)
        return super().put(request, *args, **kwargs)

    @add_bearer_security
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().delete(request, *args, **kwargs)


class GenerateReportView(APIView):  # type: ignore
    """
    Формирование отчета по пользователю за все время либо за опр. период
    """
    @swagger_auto_schema_with_types
    def post(self, request: Request, *_args: Any, **_kwargs: Any) -> Response:
        """
        POST-запрос для генерации отчета по транзакциям пользователя.
        Проверяет наличие транзакций за указанный период и инициирует задачу Celery.
        """
        user_id = request.data.get('user_id')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        transactions_exists = Transaction.objects.filter(
            user_id=user_id,
            date_transaction__range=[start_date, end_date]
        ).exists()

        if not transactions_exists:
            return Response(
                {"message": "В БД нет записей для выбранного пользователя за указанный период."},
                status=status.HTTP_404_NOT_FOUND
            )

        task = generate_transaction_report.delay(user_id=user_id,
                                                 start_date=start_date, end_date=end_date)

        return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)
