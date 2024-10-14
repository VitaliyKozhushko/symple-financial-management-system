"""
Модуль для unit-тестов модели Budget
"""
import pytest
from django.utils.timezone import now
from budget.models import Budget
from users.models import User


@pytest.mark.django_db
class TestBudgetModel:
    """
    Набор тестов для модели Budget
    """
    @pytest.fixture
    def user(self) -> User:
        """
        Создание пользователя для тестов.
        """
        return User.objects.create(
            first_name="John", last_name="Doe", email="john.doe@example.com"
        )

    @pytest.fixture
    def valid_budget_data(self, user: User) -> dict[str, object]:
        """
        Валидные данные для создания бюджета.
        """
        return {
            'user': user,
            'start_date': now(),
            'end_date': now(),
            'budget': {
                "income": {
                    "Salary": {
                        "forecast": 1000.0,
                        "actual": 800.0,
                        "is_notified": False,
                        "date_notified": None
                    }
                },
                "expense": {
                    "Food": {
                        "forecast": 300.0,
                        "actual": 250.0,
                        "is_notified": False,
                        "date_notified": None
                    }
                }
            }
        }

    def test_budget_creation(self, valid_budget_data: dict[str, object]) -> None:
        """
        Проверка успешного создания бюджета.
        """
        budget = Budget.objects.create(**valid_budget_data)
        assert budget.user.email == 'john.doe@example.com'
        assert budget.start_date is not None
        assert budget.end_date is not None
        assert "income" in budget.budget
        assert "expense" in budget.budget
        assert budget.budget['income']['Salary']['forecast'] == 1000.0

    def test_budget_str_representation(self, valid_budget_data: dict[str, object]) -> None:
        """
        Проверка строкового представления бюджета.
        """
        budget = Budget.objects.create(**valid_budget_data)
        expected_str = f"{budget.user} ({budget.start_date} - {budget.end_date})"
        assert str(budget) == expected_str

    def test_budget_structure(self, valid_budget_data: dict[str, object]) -> None:
        """
        Проверка структуры поля budget.
        """
        budget = Budget.objects.create(**valid_budget_data)
        assert isinstance(budget.budget, dict)
        assert "income" in budget.budget
        assert "Salary" in budget.budget['income']
        assert "forecast" in budget.budget['income']['Salary']
        assert budget.budget['income']['Salary']['forecast'] == 1000.0
        assert budget.budget['expense']['Food']['actual'] == 250.0

    def test_budget_notification_flag(self, valid_budget_data: dict[str, object]) -> None:
        """
        Проверка флага уведомления в бюджете.
        """
        budget = Budget.objects.create(**valid_budget_data)
        assert budget.budget['income']['Salary']['is_notified'] is False
        assert budget.budget['expense']['Food']['is_notified'] is False
