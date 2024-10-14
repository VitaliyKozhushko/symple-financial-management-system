"""
Модуль для unit-тестов модели Transaction
"""
from typing import Dict
import pytest
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from fin_transactions.models import Transaction
from users.models import User


@pytest.mark.django_db
class TestTransactionModel:
    """
    Набор тестов для модели Transaction
    """
    @pytest.fixture
    def user(self) -> User:
        """
        Создание пользователя для тестов
        """
        return User.objects.create(
            first_name="John", last_name="Doe", email="john.doe@example.com"
        )

    @pytest.fixture
    def valid_transaction_data(self, user: User) -> Dict[str, object]:
        """
        Данные для валидной транзакции
        """
        return {
            'user': user,
            'amount': 100.00,
            'transaction_type': Transaction.INCOME,
            'category': 'Salary',
            'date_transaction': now()
        }

    def test_transaction_creation(self, valid_transaction_data: Dict[str, object]) -> None:
        """
        Проверка успешного создания транзакции с валидными данными.
        """
        transaction = Transaction.objects.create(**valid_transaction_data)
        assert transaction.amount == 100.00
        assert transaction.transaction_type == Transaction.INCOME
        assert transaction.category == 'Salary'

    def test_transaction_str_representation(self,
                                            valid_transaction_data: Dict[str, object]) -> None:
        """
        Проверка строкового представления транзакции.
        """
        transaction = Transaction.objects.create(**valid_transaction_data)
        expected_str = "Доход - 100.00 (Salary)"
        assert str(transaction) == expected_str

    def test_get_transaction_type_display_custom(self,
                                                 valid_transaction_data: Dict[str, object]) -> None:
        """
        Проверка метода get_transaction_type_display_custom.
        """
        transaction = Transaction.objects.create(**valid_transaction_data)
        assert transaction.get_transaction_type_display_custom() == "Доход"

    def test_clean_method_positive_amount(self, valid_transaction_data: Dict[str, object]) -> None:
        """
        Проверка, что транзакция с отрицательной суммой вызывает ValidationError.
        """
        valid_transaction_data['amount'] = -50.00
        transaction = Transaction(**valid_transaction_data)
        with pytest.raises(ValidationError) as excinfo:
            transaction.clean()
        assert 'amount' in excinfo.value.message_dict
        assert excinfo.value.message_dict['amount'] == ['Сумма транзакции должна быть больше нуля']

    def test_transaction_with_negative_amount_should_fail(
            self,
            valid_transaction_data: Dict[str, object]) -> None:
        """
        Проверка неуспешного создания транзакции с отрицательной суммой.
        """
        valid_transaction_data['amount'] = -100.00
        transaction = Transaction(**valid_transaction_data)
        with pytest.raises(ValidationError):
            transaction.full_clean()

    def test_auto_update_date_modified(self, valid_transaction_data: Dict[str, object]) -> None:
        """
        Проверка автоматического обновления поля date_modified при изменении транзакции.
        """
        transaction = Transaction.objects.create(**valid_transaction_data)
        initial_date_modified = transaction.date_modified

        transaction.amount = 200.00
        transaction.save()

        assert transaction.date_modified > initial_date_modified
