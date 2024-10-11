"""
Модуль для сериализаторов модели User
"""
from typing import (Dict,
                    Any)
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):  # type: ignore
    """
    Класс сериализатора для регистрации пользователя
    """
    password = serializers.CharField(write_only=True)

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Класс настройки сериализатора регистрации пользователя
        """
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data: Dict[str, Any]) -> User:
        user = User(
            username=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):  # type: ignore
    """
    Класс сериализатора для списка пользователей и данных по опр. пользователю
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Класс настройки сериализатора регистрации пользователя
        """
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'date_joined']
