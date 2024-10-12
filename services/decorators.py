"""Модуль для различных декораторов"""
from typing import (Any,
                    cast,
                    Callable,
                    TypeVar)
from functools import wraps
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

F = TypeVar('F', bound=Callable[..., Response])


def add_bearer_security(view_method: F) -> F:
    """Декоратор добавления Bearer токена в аннотацию swagger_auto_schema"""

    @wraps(view_method)
    def wrapper(*args: Any, **kwargs: Any) -> Response:
        return view_method(*args, **kwargs)

    return cast(F, swagger_auto_schema(security=[{'Bearer': []}])(wrapper))


def swagger_auto_schema_with_types(func: F) -> F:
    """Декоратор добавления схемы API для генерации отчета"""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Response:
        return func(*args, **kwargs)

    return cast(F, swagger_auto_schema(security=[{'Bearer': []}],
                                       operation_description=("Генерация отчета по "
                                                              "транзакциям пользователя"),
                                       request_body=openapi.Schema(
                                           type=openapi.TYPE_OBJECT,
                                           properties={
                                               'user_id': openapi.Schema(
                                                   type=openapi.TYPE_INTEGER,
                                                   description='ID пользователя'),
                                               'start_date': openapi.Schema(
                                                   type=openapi.TYPE_STRING,
                                                   format='date',
                                                   description='Дата начала (YYYY-MM-DD)'),
                                               'end_date': openapi.Schema(
                                                   type=openapi.TYPE_STRING,
                                                   format='date',
                                                   description='Дата окончания (YYYY-MM-DD)')
                                           },
                                           required=['user_id']
                                       ),
                                       responses={
                                           202: openapi.Response('Accepted', openapi.Schema(
                                               type=openapi.TYPE_OBJECT,
                                               properties={
                                                   'task_id': openapi.Schema(
                                                       type=openapi.TYPE_STRING,
                                                       description='ID задачи Celery')
                                               }
                                           )),
                                       })(wrapper))
