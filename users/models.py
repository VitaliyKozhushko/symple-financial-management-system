"""
Модуль моделей приложения users для хранения информации о пользователях в БД
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Модель пользователя

    Поля:
        first_name (str): имя пользователя
        last_name (str): фамилия пользователя
        email (str): уникальный email пользователя
        date_joined (datetime): дата и время регистрации пользователя
        date_modified (datetime): дата и время последнего изменения данных пользователя
    """
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Email')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    date_modified = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Уст. название таблицы в БД, человекочитаемое название модели
        """
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        """
        Возвращает строковое представление пользователя, состоящее из имени и фамилии.
        """
        return f"{self.first_name} {self.last_name}"
