"""
Модуль для тестирования сохранения отчета в csv-файл и отправки на email
"""
import os
import pytest
from django.core import mail
from services.email import add_file
from users.models import User
from fin_transactions.models import Transaction
from fin_transactions.celery_tasks import generate_transaction_report


@pytest.mark.django_db
class TestGenerateTransactionReport:
    """
    Набор тестов для проверки генерации отчета
    """

    @pytest.fixture
    def user(self) -> User:
        """
        Фикстура для создания пользователя
        """
        return User.objects.create(
            first_name='Test', last_name='User', email='itvkip@yandex.ru', password="testpassword"
        )

    @pytest.fixture
    def transactions(self, user: User) -> list[Transaction]:
        """
        Фикстура для создания транзакций
        """
        return [
            Transaction.objects.create(
                user=user,
                amount=100,
                transaction_type="INCOME",
                category="Salary",
                date_transaction="2024-01-01T00:01Z"
            ),
            Transaction.objects.create(
                user=user,
                amount=200,
                transaction_type="EXPENSE",
                category="Groceries",
                date_transaction="2024-01-02T00:01Z"
            )
        ]

    def test_generate_report_send_email(self, user: User, transactions: list[Transaction]) -> None:
        """
        Проверка для фактического выполнения Celery задачи и отправки отчета на email
        """
        assert transactions is not None

        mail.outbox = []

        result = generate_transaction_report.apply(args=[user.id, "2024-01-01", "2024-12-31", True])

        assert result.status == 'SUCCESS'

        assert len(mail.outbox) == 1
        email = mail.outbox[0]

        assert email.subject == 'Ваш отчет по транзакциям'
        assert 'Отчет по вашим транзакциям прикреплен к этому письму.' in email.body
        assert email.to == [user.email]

        assert len(email.attachments) == 1
        attachment = email.attachments[0]

        assert attachment[0] == 'transaction_report.csv'
        assert attachment[2] == 'text/csv, charset=utf-8'

        csv_content = attachment[1]

        expected_csv_header = 'Имя,Фамилия,Email,Сумма,Тип транзакции,Категория,Дата\n'
        expected_csv_row_1 = 'Test,User,itvkip@yandex.ru,100.00,INCOME,Salary,2024-01-01\n'
        expected_csv_row_2 = 'Test,User,itvkip@yandex.ru,200.00,EXPENSE,Groceries,2024-01-02\n'

        assert expected_csv_header in csv_content
        assert expected_csv_row_1 in csv_content
        assert expected_csv_row_2 in csv_content

    def test_generate_report_save_csv(self, user: User, transactions: list[Transaction]) -> None:
        """
        Проверка для фактического выполнения Celery задачи и сохранения отчета локально
        """
        assert transactions is not None

        result = generate_transaction_report.apply(
            args=[user.id, "2024-01-01", "2024-12-31", False])

        assert result.status == 'SUCCESS'
        assert result.result is not None

        saved_file_path = result.result
        assert os.path.exists(saved_file_path)

        if os.path.exists(saved_file_path):
            os.remove(saved_file_path)

    def test_add_file(self) -> None:
        """
        Проверка корректности создания файла для отправки
        """
        file_content = [['Имя', 'Фамилия', 'Email', 'Сумма'],
                        ['Test', 'User', 'test@example.com', '100']]

        result = add_file(file_content)

        expected_result = ('Имя,Фамилия,Email,Сумма\nTest,'
                           'User,test@example.com,100\n').encode('utf-8')

        assert result == expected_result
