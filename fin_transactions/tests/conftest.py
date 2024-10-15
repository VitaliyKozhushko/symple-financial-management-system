"""
Общие фикстуры для тестов формирования отчетов и транзакций
"""
import pytest
from users.models import User


@pytest.fixture
def user() -> User:
    """
    Фикстура для создания пользователя.
    """
    return User.objects.create(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com"
    )
