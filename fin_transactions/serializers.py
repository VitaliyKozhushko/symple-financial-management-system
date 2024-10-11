"""
Модуль для сериализаторов модели Transaction
"""
from rest_framework import serializers
from .models import Transaction


class TransactionsSerializer(serializers.ModelSerializer):  # type: ignore
    """
    Класс сериализатора для работы с моделью
    """
    class Meta:  # pylint: disable=too-few-public-methods
        """
        Класс настройки сериализатора транзакций
        """
        model = Transaction
        fields = ['id', 'user', 'amount', 'transaction_type', 'category', 'date_transaction']
