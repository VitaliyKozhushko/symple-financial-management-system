"""
Модуль для unit-тестов API User
"""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User


@pytest.mark.django_db
class TestUserAPI:
    """
    Набор тестов для API User
    """

    @pytest.fixture
    def api_client(self) -> APIClient:
        """
        Фикстура для клиента API
        """
        return APIClient()

    @pytest.fixture
    def created_user(self, api_client: APIClient) -> dict[str, User]:
        """
        Фикстура для создания пользователя, который будет использоваться в тестах.
        """
        url = reverse('user-list-create')
        user_1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "secure_password"
        }
        user_2 = {
            "first_name": "John1",
            "last_name": "Doe1",
            "email": "john.doe1@example.com",
            "password": "secure1_password"
        }

        response1 = api_client.post(url, user_1, format='json')
        assert response1.status_code == status.HTTP_201_CREATED

        response2 = api_client.post(url, user_2, format='json')
        assert response2.status_code == status.HTTP_201_CREATED

        return {
            'user_1' : User.objects.get(email="john.doe@example.com"),
            'user_2': User.objects.get(email="john.doe1@example.com"),
        }

    def test_update_user(self, api_client: APIClient, created_user: dict[str, User]) -> None:
        """
        Тестирование редактирования пользователя
        """
        url = reverse('user-detail-update-delete', args=[created_user['user_1'].id])

        updated_data = {
            "first_name": "Johnny",
            "last_name": "Doe"
        }

        api_client.force_authenticate(user=created_user['user_1'])
        response = api_client.put(url, updated_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['first_name'] == "Johnny"

    def test_delete_user(self, api_client: APIClient, created_user: dict[str, User]) -> None:
        """
        Тестирование удаления пользователя
        """
        url = reverse('user-detail-update-delete', args=[created_user['user_2'].id])

        api_client.force_authenticate(user=created_user['user_1'])
        response = api_client.delete(url)
        print(response.data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
