"""
Модуль для представлений модели Transaction
"""
from typing import (Any,
                    cast,
                    Callable,
                    TypeVar)
from functools import wraps
from decimal import (Decimal,
                     InvalidOperation)
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionsSerializer

F = TypeVar('F', bound=Callable[..., Response])


def add_bearer_security(view_method: F) -> F:
    """Декоратор добавления Bearer токена в аннотацию swagger_auto_schema"""

    @wraps(view_method)
    def wrapper(*args: Any, **kwargs: Any) -> Response:
        return view_method(*args, **kwargs)

    return cast(F, swagger_auto_schema(security=[{'Bearer': []}])(wrapper))


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
        try:
            amount = Decimal(request.data.get('amount', '0'))
        except (ValueError, TypeError, InvalidOperation) as err:
            raise ValidationError({"amount": "Сумма транзакции должна быть числом."}) from err
        if amount <= 0:
            raise ValidationError({"amount": "Сумма транзакции должна быть больше нуля"})
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
        try:
            amount = Decimal(request.data.get('amount', '0'))
        except (ValueError, TypeError, InvalidOperation) as err:
            raise ValidationError({"amount": "Сумма транзакции должна быть числом."}) from err
        if amount <= 0:
            raise ValidationError({"amount": "Сумма транзакции должна быть больше нуля"})
        return super().put(request, *args, **kwargs)

    @add_bearer_security
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().delete(request, *args, **kwargs)
