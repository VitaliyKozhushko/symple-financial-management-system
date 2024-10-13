"""
Модуль для представлений модели Transaction
"""
from typing import Any
from decimal import (Decimal,
                     InvalidOperation)
from celery.result import AsyncResult
from rest_framework import (generics,
                            status)
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from services.decorators import (add_bearer_security,
                                 swagger_auto_schema_with_types)
from .celery_tasks import generate_transaction_report
from .models import (Transaction,
                     ReportsResult)
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
        send_email = bool(request.data.get('send_email', False))

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
                                                 start_date=start_date,
                                                 end_date=end_date,
                                                 send_email=send_email)

        return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)


class ReportDownloadView(APIView):  # type: ignore
    """
    Получение готового отчета по транзакциям
    """

    @staticmethod
    def get(request: Request, task_id: str, *_args: Any, **_kwargs: Any) -> Response:
        """Получение статуса формирования отчета и готового результата (при сохранении CSV в БД)"""
        try:
            report_result = ReportsResult.objects.get(task_id=task_id)
            task_result = AsyncResult(task_id)
            task_status = task_result.state

            status_messages = {
                'PENDING': 'Формирование отчета в очереди на выполнение',
                'STARTED': 'Формирование отчета выполняется',
                'FAILURE': 'Ошибка при формирвании отчета'
            }

            if task_status in status_messages:
                return Response(
                    {'status': status_messages[task_status]},
                    status=(status.HTTP_200_OK if task_status != 'FAILURE'
                            else status.HTTP_500_INTERNAL_SERVER_ERROR)
                )

            if task_status == 'SUCCESS' and report_result.status == 'completed':
                if report_result.send_email:
                    return Response({
                        'status': f'Отчет успешно отправлен на email {report_result.user.email}'
                    }, status=status.HTTP_200_OK)

                return Response({
                    'status': 'Формирование отчета выполнено',
                    'file_url': request.build_absolute_uri(
                        f'{settings.MEDIA_URL}reports/{report_result.report}'
                    )
                }, status=status.HTTP_200_OK)

            return Response({'status': 'Формирование отчета в процессе'}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'status': 'Задача по формированию отчета не найдена'},
                            status=status.HTTP_404_NOT_FOUND)
