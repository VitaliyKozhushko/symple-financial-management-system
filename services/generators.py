"""Модуль для различных генераторов"""
from typing import (Any,
                    cast,
                    Callable,
                    TypeVar)
from functools import wraps
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

F = TypeVar('F', bound=Callable[..., Response])


def add_bearer_security(view_method: F) -> F:
    """Декоратор добавления Bearer токена в аннотацию swagger_auto_schema"""

    @wraps(view_method)
    def wrapper(*args: Any, **kwargs: Any) -> Response:
        return view_method(*args, **kwargs)

    return cast(F, swagger_auto_schema(security=[{'Bearer': []}])(wrapper))
