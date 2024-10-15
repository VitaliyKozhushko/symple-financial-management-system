"""
Модуль для unit-тестов API Transaction
"""
import pytest
from django.urls import reverse
from django.utils import timezone as django_timezone
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from fin_transactions.models import Transaction


@pytest.mark.django_db
class TestBudgetAPI:
    """
    Набор тестов для API Transaction
    """

    @pytest.fixture
    def api_client(self) -> APIClient:
        """
        Фикстура для клиента API
        """
        return APIClient()

    @pytest.fixture
    def transaction(self, user: User) -> Transaction:
        """
        Фикстура для создания транзакции
        """
        return Transaction.objects.create(
            user=user,
            amount='100.00',
            transaction_type=Transaction.INCOME,
            category='Salary',
            date_transaction=django_timezone.now()
        )

    def test_create_transaction(self, api_client: APIClient, user: User) -> None:
        """
        Проверка создания транзакции
        """
        api_client.force_authenticate(user=user)
        url = reverse('transaction-list-create')
        data = {
            'user': user.id,
            'amount': '150.00',
            'transaction_type': Transaction.INCOME,
            'category': 'Bonus',
            'date_transaction': '2023-10-10T10:00Z'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['amount'] == '150.00'
        assert response.data['category'] == 'Bonus'

    def test_get_transaction_list(self, api_client: APIClient, transaction: Transaction,
                                  user: User) -> None:
        """
        Проверка получения списка транзакций
        """
        api_client.force_authenticate(user=user)
        url = reverse('transaction-list-create')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == transaction.id

    def test_get_transaction_detail(self, api_client: APIClient, transaction: Transaction,
                                    user: User) -> None:
        """
        Проверка получения данных опр. транзакции
        """
        api_client.force_authenticate(user=user)
        url = reverse('transaction-detail-update-delete', args=[transaction.id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == transaction.id
        assert response.data['amount'] == transaction.amount

    def test_update_transaction(self, api_client: APIClient, transaction: Transaction,
                                user: User) -> None:
        """
        Проверка обновления транзакции
        """
        api_client.force_authenticate(user=user)
        url = reverse('transaction-detail-update-delete', args=[transaction.id])
        data = {
            'user': user.id,
            'amount': '200.00',
            'transaction_type': Transaction.INCOME,
            'category': 'Updated Salary',
            'date_transaction': '2023-10-11T12:00Z'
        }
        response = api_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['amount'] == '200.00'
        assert response.data['category'] == 'Updated Salary'

    def test_delete_transaction(self, api_client: APIClient, transaction: Transaction,
                                user: User) -> None:
        """
        Проверка удаления транзакции
        """
        api_client.force_authenticate(user=user)
        url = reverse('transaction-detail-update-delete', args=[transaction.id])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Transaction.objects.filter(id=transaction.id).exists()
