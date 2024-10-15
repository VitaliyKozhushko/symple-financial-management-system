"""
Модуль для unit-тестов API отчетов
"""
from unittest.mock import patch, Mock, MagicMock
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from fin_transactions.models import (Transaction,
                                     ReportsResult)
from users.models import User


@pytest.mark.django_db
class TestReportAPI:
    """
    Набор интеграционных тестов для API генерации отчета
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
        Фикстура для создания пользователя
        """
        return User.objects.create(
            first_name='John', last_name='Doe', email='johndoe@example.com'
        )

    @pytest.fixture
    def transaction(self, user: User) -> Transaction:
        """
        Фикстура для создания транзакции для пользователя
        """
        return Transaction.objects.create(
            user=user,
            amount=100,
            transaction_type=Transaction.INCOME,
            category="Salary",
            date_transaction="2024-10-01T00:00Z"
        )

    @patch('fin_transactions.celery_tasks.generate_transaction_report.delay')
    def test_generate_report(self, mock_generate_transaction_report_delay: MagicMock,
                             api_client: APIClient, user: User, transaction: Transaction) -> None:
        """
        Проверка генерации отчета через API и запуска задачи Celery
        """
        assert transaction is not None

        mock_generate_transaction_report_delay.return_value = Mock(id='test-task-id')

        api_client.force_authenticate(user=user)
        url = reverse('generate_report')
        data = {
            'user_id': user.id,
            'start_date': '2024-01-01T01:01Z',
            'end_date': '2024-12-31T01:01Z',
            'send_email': True
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert 'task_id' in response.data

        mock_generate_transaction_report_delay.assert_called_once_with(
            user_id=user.id,
            start_date='2024-01-01T01:01Z',
            end_date='2024-12-31T01:01Z',
            send_email=True
        )

        assert mock_generate_transaction_report_delay.called

    def test_generate_report_no_transactions(self, api_client: APIClient, user: User) -> None:
        """
        Проверка случая, когда нет транзакций за указанный период
        """
        api_client.force_authenticate(user=user)
        url = reverse('generate_report')
        data = {
            'user_id': user.id,
            'start_date': '2024-01-01T01:01Z',
            'end_date': '2024-12-31T01:01Z',
            'send_email': True
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['message'] == ("В БД нет записей для выбранного "
                                            "пользователя за указанный период.")

    @pytest.fixture
    def create_report(self, user: User) -> ReportsResult:
        """
        Фикстура для создания результата отчета
        """
        return ReportsResult.objects.create(
            user=user,
            task_id="some-task-id",
            report="Отчет по транзакциям",
            send_email=True,
            status="SUCCESS",
            error_message="",
        )

    def test_report_result(self, api_client: APIClient, user: User,
                           create_report: ReportsResult) -> None:
        """
        Проверка сохранения результата отчета в модели ReportsResult
        """
        assert create_report is not None

        api_client.force_authenticate(user=user)
        report = ReportsResult.objects.filter(user=user).first()

        assert report is not None
        assert report.task_id == "some-task-id"
        assert report.status == "SUCCESS"
        assert report.report == "Отчет по транзакциям"
