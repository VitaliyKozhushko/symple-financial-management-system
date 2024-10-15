"""
Модуль для unit-тестов модели ReportsResult
"""
from typing import Dict
import pytest
from django.utils.timezone import now
from fin_transactions.models import ReportsResult
from users.models import User


@pytest.mark.django_db
class TestReportsResultModel:
    """
    Набор тестов для модели ReportsResult
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
    def report_result_data(self, user: User) -> Dict[str, object]:
        """
        Данные для создания отчета
        """
        return {
            'user': user,
            'task_id': '123456',
            'report': '/path/to/report',
            'send_email': True,
            'status': 'in_progress',
            'error_message': None,
            'created_at': now().date()
        }

    def test_report_creation(self, report_result_data: Dict[str, object]) -> None:
        """
        Проверка успешного создания отчета.
        """
        report = ReportsResult.objects.create(**report_result_data)
        assert report.user.email == 'john.doe@example.com'
        assert report.task_id == '123456'
        assert report.report == '/path/to/report'
        assert report.send_email is True
        assert report.status == 'in_progress'

    def test_report_str_representation(self, report_result_data: Dict[str, object]) -> None:
        """
        Проверка строкового представления отчета.
        """
        report = ReportsResult.objects.create(**report_result_data)
        expected_str = f"Task 123456 for user {report.user}"
        assert str(report) == expected_str

    def test_report_status_choices(self, report_result_data: Dict[str, object]) -> None:
        """
        Проверка изменения статуса отчета.
        """
        report = ReportsResult.objects.create(**report_result_data)
        report.status = 'completed'
        report.save()
        assert report.status == 'completed'

    def test_report_error_message(self, report_result_data: Dict[str, object]) -> None:
        """
        Проверка записи сообщения об ошибке.
        """
        report_result_data['status'] = 'error'
        report_result_data['error_message'] = 'Some error occurred'
        report = ReportsResult.objects.create(**report_result_data)
        assert report.status == 'error'
        assert report.error_message == 'Some error occurred'
