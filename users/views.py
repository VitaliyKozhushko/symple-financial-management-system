"""
Модуль для представлений модели User
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer


class RegisterUserView(APIView):  # type: ignore
    """
    Класс представления для регистрации пользователя
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserSerializer)  # type: ignore
    def post(self, request: Request) -> Response:
        """
        POST-запрос регистрации нового пользователя
        Аргументы:
            request (Request): запрос, содержащий данные для регистрации пользователя.

        Возвращает:
            Response: Ответ с сообщением об успешной регистрации или с ошибками валидации.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
