"""
Модуль для unit-тестов API получения статуса задачи формирования отчета
"""
from unittest.mock import (MagicMock,
                           patch)
from typing import Callable
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from fin_transactions.models import ReportsResult
from users.models import User


@pytest.mark.django_db
class TestReportDownloadAPI:
    """
    Набор тестов для API получения статуса задачи формирования отчета
    """

    @pytest.fixture
    def api_client(self) -> APIClient:
        """
        Фикстура для клиента API
        """
        return APIClient()

    @pytest.fixture
    def report_result(self, user: User) -> Callable[[str], ReportsResult]:
        """
        Фикстура для создания отчета в БД с возможностью указать статус.
        Возвращает функцию, которая создаёт отчёт с заданным статусом.
        """

        def create_report(status_report: str) -> ReportsResult:
            return ReportsResult.objects.create(
                user=user,
                task_id="1234",
                report="test_report.csv",
                send_email=False,
                status=status_report
            )

        return create_report

    @patch('fin_transactions.views.AsyncResult')
    def test_report_download_success(self, mock_async_result: MagicMock, api_client: APIClient,
                                     user: User,
                                     report_result: Callable[[str], ReportsResult]) -> None:
        """
        Проверка успешного получения отчета через API
        """
        report = report_result('completed')

        mock_async_result_instance = mock_async_result.return_value
        mock_async_result_instance.state = 'SUCCESS'

        api_client.force_authenticate(user=user)
        url = reverse('report_download', args=[report.task_id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'Формирование отчета выполнено'
        assert 'file_url' in response.data

    @patch('fin_transactions.views.AsyncResult')
    def test_report_download_pending(self, mock_async_result: MagicMock,
                                     api_client: APIClient, user: User,
                                     report_result: Callable[[str], ReportsResult]) -> None:
        """
        Проверка получения отчета в состоянии 'PENDING'
        """
        report = report_result("in_progress")

        mock_async_result_instance = mock_async_result.return_value
        mock_async_result_instance.state = 'PENDING'

        api_client.force_authenticate(user=user)
        url = reverse('report_download', args=[report.task_id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'Формирование отчета в очереди на выполнение'

    @patch('fin_transactions.views.AsyncResult')
    def test_report_download_failure(self, mock_async_result: MagicMock,
                                     api_client: APIClient, user: User,
                                     report_result: Callable[[str], ReportsResult]) -> None:
        """
        Проверка получения отчета в состоянии 'FAILURE'
        """
        report = report_result("failed")

        mock_async_result_instance = mock_async_result.return_value
        mock_async_result_instance.state = 'FAILURE'

        api_client.force_authenticate(user=user)

        url = reverse('report_download', args=[report.task_id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data['status'] == 'Ошибка при формирвании отчета'

    def test_report_download_not_found(self, api_client: APIClient, user: User) -> None:
        """
        Проверка для несуществующей задачи
        """
        api_client.force_authenticate(user=user)
        url = reverse('report_download', args=["non_existent_task_id"])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'Задача по формированию отчета не найдена'
