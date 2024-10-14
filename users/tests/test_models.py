"""
Модуль для unit-тестов модели User
"""
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """
    Класс тестирования модели User
    """
    def test_create_user(self) -> None:
        """
        Тестирование создания пользователя
        """
        user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="strong_password"
        )
        assert user.email == "john.doe@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.check_password("strong_password")

    def test_create_superuser(self) -> None:
        """
        Тестирование создания суперпользователя
        """
        superuser = User.objects.create_superuser(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            password="super_password"
        )
        assert superuser.is_superuser
        assert superuser.is_staff
        assert superuser.email == "admin@example.com"

    def test_user_str_method(self) -> None:
        """
        Тестирование вывода данных о пользователе
        """
        user = User.objects.create_user(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            password="another_password"
        )
        assert str(user) == "Jane Smith"

    def test_unique_email_constraint(self) -> None:
        """
        Тестирование уникальности email
        """
        User.objects.create_user(
            first_name="Alice",
            last_name="Wonder",
            email="alice@example.com",
            password="password1"
        )
        with pytest.raises(Exception):
            User.objects.create_user(
                first_name="Bob",
                last_name="Builder",
                email="alice@example.com",
                password="password2"
            )
