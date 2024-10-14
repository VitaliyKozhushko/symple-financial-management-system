"""
Модуль моделей приложения users для хранения информации о пользователях в БД
"""
from typing import TypeVar, Optional, Any, Generic, ClassVar
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

UserModel = TypeVar('UserModel', bound='User')


class CustomUserManager(BaseUserManager[UserModel], Generic[UserModel]):
    """
    Класс кастомного менеджера моделей
    """
    def create_user(self, email: str, first_name: str, last_name: str,
                    password: Optional[str] = None,
                    **extra_fields: Any) -> UserModel:
        """
        Создание обычного пользователя, не требующего username.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, first_name: str, last_name: str,
                         password: Optional[str] = None,
                         **extra_fields: Any) -> UserModel:
        """
            Создание супер пользователя, не требующего username.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, first_name, last_name, password, **extra_fields)


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

    objects: ClassVar[CustomUserManager['User']] = CustomUserManager()  # type: ignore

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
