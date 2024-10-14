"""
Модуль для unit-тестов API Budget
"""
from typing import Any
from datetime import timedelta
import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from budget.models import Budget
from .constants import BUDGET


@pytest.mark.django_db
class TestBudgetAPI:
    """
    Набор тестов для API Budget
    """
    @pytest.fixture
    def api_client(self) -> APIClient:
        """
        Фикстура для клиента API
        """
        return APIClient()

    @pytest.fixture
    def user(self) -> User:
        """
        Создание пользователя для тестов
        """
        return User.objects.create(
            first_name="John", last_name="Doe", email="john.doe@example.com"
        )

    @pytest.fixture
    def valid_budget_data(self, user: User) -> dict[str, Any]:
        """
        Валидные данные для создания бюджета
        """
        return {
            'user': user.id,
            'start_date': timezone.now(),
            'end_date': timezone.now() + timedelta(days=30),
            'budget': BUDGET
        }

    def test_create_budget(self, api_client: APIClient,
                           user: User, valid_budget_data: dict[str, Any]) -> None:
        """
        Проверка создания бюджета
        """
        api_client.force_authenticate(user=user)
        response = api_client.post(reverse('budget-list-create'), valid_budget_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Budget.objects.count() == 1
        assert Budget.objects.get().user == user

    def test_get_budget_list(self, api_client: APIClient,
                             user: User, valid_budget_data: dict[str, Any]) -> None:
        """
        Проверка получения списка бюджетов
        """
        api_client.force_authenticate(user=user)
        api_client.post(reverse('budget-list-create'), valid_budget_data, format='json')

        response = api_client.get(reverse('budget-list-create'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_get_budget_detail(self, api_client: APIClient,
                               user: User, valid_budget_data: dict[str, Any]) -> None:
        """
        Проверка получения деталей конкретного бюджета
        """
        api_client.force_authenticate(user=user)
        valid_budget_data.pop('user', None)
        budget = Budget.objects.create(user=user, **valid_budget_data)

        response = api_client.get(reverse('budget-detail', args=[budget.id]), format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == budget.id

    def test_update_budget(self, api_client: APIClient,
                           user: User, valid_budget_data: dict[str, Any]) -> None:
        """
        Проверка обновления бюджета
        """
        api_client.force_authenticate(user=user)
        valid_budget_data['user'] = user
        budget = Budget.objects.create(**valid_budget_data)

        updated_data = {
            **valid_budget_data,
            'user': user.id,
            'budget': {
                "income": {
                    "Salary": {
                        "forecast": 1200.0,  # Изменено значение
                        "actual": 900.0,
                        "is_notified": False,
                        "date_notified": None
                    }
                },
                "expense": {
                    "Food": {
                        "forecast": 400.0,  # Изменено значение
                        "actual": 300.0,
                        "is_notified": False,
                        "date_notified": None
                    }
                }
            }
        }

        response = api_client.put(reverse('budget-detail',
                                          args=[budget.id]), updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        budget.refresh_from_db()
        assert budget.budget['income']['Salary']['forecast'] == 1200.0
        assert budget.budget['expense']['Food']['forecast'] == 400.0

    def test_delete_budget(self, api_client: APIClient,
                           user: User, valid_budget_data: dict[str, Any]) -> None:
        """
        Проверка удаления бюджета
        """
        api_client.force_authenticate(user=user)
        valid_budget_data['user'] = user
        budget = Budget.objects.create(**valid_budget_data)

        response = api_client.delete(reverse('budget-detail', args=[budget.id]), format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Budget.objects.count() == 0
