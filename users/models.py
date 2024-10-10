"""
Модуль моделей приложения User для хранения информации о пользователях в базе данных.
"""
from django.db import models


class User(models.Model):
    """
    Модель пользователя

    Атрибуты:
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

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Определяет метаданные модели User. На данный момент - название таблицы в БД
        """
        db_table = 'users'

    def __str__(self) -> str:
        """
        Возвращает строковое представление пользователя, состоящее из имени и фамилии.

        Returns:
            str: имя и фамилия пользователя
        """
        return f"{self.first_name} {self.last_name}"
