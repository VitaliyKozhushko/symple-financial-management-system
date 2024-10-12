"""
Модуль для сериализаторов модели Transaction
"""
from typing import (Dict,
                    Any,
                    cast)
from datetime import (datetime,
                      timezone)
from rest_framework import serializers
from django.utils import timezone as django_timezone
from .models import Transaction


class TransactionsSerializer(serializers.ModelSerializer):  # type: ignore
    """
    Класс сериализатора для работы с моделью
    """

    date_transaction = serializers.CharField(required=False, allow_blank=True)

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Класс настройки сериализатора транзакций
        """
        model = Transaction
        fields = ['id', 'user', 'amount', 'transaction_type', 'category', 'date_transaction']

    @staticmethod
    def validate_date_transaction(value: str) -> datetime:
        """
        Проверка и обработка формата даты.
        1. Если дата передана в формате 'YYYY-MM-DDTHH:MMZ', парсим её.
        2. Если передана пустая строка (""), устанавливаем текущую дату.
        3. Если поле не передано, это обрабатывается в методах create/update.
        """
        if value is None or value == "":
            # Если значение None или пустая строка, возвращаем текущую дату
            return django_timezone.now()

        try:
            # Парсим дату, если она передана в формате без секунд и миллисекунд
            parsed_value = datetime.strptime(value, '%Y-%m-%dT%H:%MZ')
            # Преобразуем дату с учетом UTC
            return django_timezone.make_aware(parsed_value, timezone=timezone.utc)
        except ValueError as err:
            # Если формат не соответствует, бросаем ошибку
            raise serializers.ValidationError(
                {
                    "date_transaction": (
                        "Неверный формат даты. "
                        "Используйте формат: YYYY-MM-DDTHH:MMZ."
                    )
                }
            ) from err

    def create(self, validated_data: Dict[str, Any]) -> Transaction:
        # Если 'date_transaction' отсутствует в запросе, устанавливаем текущую дату
        validated_data['date_transaction'] = validated_data.get('date_transaction',
                                                                django_timezone.now())
        return cast(Transaction, super().create(validated_data))

    def update(self, instance: Transaction, validated_data: Dict[str, Any]) -> Transaction:
        # Если 'date_transaction' отсутствует в запросе, устанавливаем текущую дату
        validated_data['date_transaction'] = validated_data.get('date_transaction',
                                                                django_timezone.now())
        return cast(Transaction, super().update(instance, validated_data))
