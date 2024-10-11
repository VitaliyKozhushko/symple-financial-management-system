"""
Модуль для представлений модели Transaction
"""
from typing import Any
from decimal import (Decimal,
                     InvalidOperation)
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from services.generators import add_bearer_security
from .models import Transaction
from .serializers import TransactionsSerializer


def validate_amount(data: dict[str, Any]) -> Decimal:
    """
        Проверяет, что сумма (amount) является числом и больше нуля.
        Возвращает значение суммы как Decimal, если проверка пройдена.

        Аргументы:
            data (dict[str, Any]): данные запроса
        Исключения:
            ValidationError: если сумма не является числом или меньше либо равна нулю
        Возвращает:
            Decimal: проверенное значение 'amount'
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
