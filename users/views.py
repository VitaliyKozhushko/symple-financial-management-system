"""
Модуль для представлений модели User
"""
from typing import (Any,
                    List,
                    Type)
from rest_framework import (generics,
                            status)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny,
                                        BasePermission,
                                        IsAuthenticated)
from rest_framework.serializers import Serializer
from services.decorators import add_bearer_security
from .serializers import (UserSerializer,
                          UserDetailSerializer)
from .models import User


class UserListView(generics.ListCreateAPIView):  # type: ignore
    """
    Получение списка пользователей и создание пользователя
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self) -> List[BasePermission]:
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self) -> Type[Serializer]:
        if self.request.method == 'POST':
            return UserSerializer
        return UserDetailSerializer

    @add_bearer_security
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)

    @add_bearer_security
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().post(request, *args, **kwargs)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):  # type: ignore
    """
    Получение данных по опр. пользователю, редактирование пользователя и его удаления
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'delete']

    @add_bearer_security
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь успешно обновлен"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @add_bearer_security
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
