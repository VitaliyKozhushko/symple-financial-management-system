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
    def created_user(self, api_client: APIClient) -> User:
        """
        Фикстура для создания пользователя, который будет использоваться в тестах.
        """
        url = reverse('user-list-create')
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "secure_password"
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        return User.objects.get(email="john.doe@example.com")

    def test_update_user(self, api_client: APIClient, created_user: User) -> None:
        """
        Тестирование редактирования пользователя
        """
        url = reverse('user-detail-update-delete', args=[created_user.id])

        updated_data = {
            "first_name": "Johnny",
            "last_name": "Doe"
        }

        api_client.force_authenticate(user=created_user)
        response = api_client.put(url, updated_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['first_name'] == "Johnny"

    def test_delete_user(self, api_client: APIClient, created_user: User) -> None:
        """
        Тестирование удаления пользователя
        """
        url = reverse('user-detail-update-delete', args=[created_user.id])

        api_client.force_authenticate(user=created_user)
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
