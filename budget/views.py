from typing import (Any,
                    Type)
from rest_framework import generics, serializers
from rest_framework.request import Request
from rest_framework.response import Response
from django.db import transaction as db_transaction
from services.decorators import add_bearer_security
from .models import Budget
from .serializers import (BudgetListSerializer,
                          BudgetDetailSerializer)


class BudgetListCreateView(generics.ListCreateAPIView):  # type: ignore
    queryset = Budget.objects.all()

    def get_serializer_class(self) -> Type[serializers.Serializer]:
        if self.request.method == 'GET':
            return BudgetListSerializer
        return BudgetDetailSerializer

    @add_bearer_security
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)

    @add_bearer_security
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        with db_transaction.atomic():
            response = super().post(request, *args, **kwargs)
            # Логика обновления бюджета тут не нужна
        return response


class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):  # type: ignore
    queryset = Budget.objects.all()
    serializer_class = BudgetDetailSerializer
    http_method_names = ['get', 'put', 'delete']

    @add_bearer_security
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)

    @add_bearer_security
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        with db_transaction.atomic():
            response = super().put(request, *args, **kwargs)
        return response

    @add_bearer_security
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        with db_transaction.atomic():
            response = super().delete(request, *args, **kwargs)
        return response
