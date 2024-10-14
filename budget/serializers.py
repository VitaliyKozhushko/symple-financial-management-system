"""
Модуль для сериализаторов модели Budget
"""
from typing import Any, Dict
from rest_framework import serializers
from .models import Budget


class BudgetListSerializer(serializers.ModelSerializer):  # type: ignore
    """
    Класс сериализатора для получения списка бюджетов
    """
    class Meta:  # pylint: disable=too-few-public-methods
        """
        Класс настройки сериализатора списка бюджетов
        """
        model = Budget
        fields = ['id', 'start_date', 'end_date']


class BudgetDetailSerializer(serializers.ModelSerializer):  # type: ignore
    """
    Класс сериализатора для получения списка опр. бюджета, редактирования бюджета целиком
    и удаления бюджета
    """
    class Meta:  # pylint: disable=too-few-public-methods
        """
        Класс настройки сериализатора опр. бюджета для чтения, редактирования и удаления
        """
        model = Budget
        fields = '__all__'

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Проверка дат и структуры бюджета
        """
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        user = attrs.get('user')

        request_method = self.context['request'].method

        if request_method == 'POST' and start_date and end_date:
            # Проверка дат начала и окончания
            if end_date <= start_date:
                raise serializers.ValidationError(
                    {'message': "Дата окончания бюджета должна быть позже даты начала."})

            # Проверка предыдущего бюджета (чтобы дата начала нового бюджета
            # была после завершения предыдущего)
            last_budget = Budget.objects.filter(user=user).order_by('-end_date').first()
            if last_budget and start_date <= last_budget.end_date:
                raise serializers.ValidationError(
                    {'message': (
                        "Дата начала бюджета должна следовать "
                        "за датой завершения предыдущего бюджета."
                    )})

        # Проверка структуры поля budget
        budget_data = attrs.get('budget')
        if not isinstance(budget_data, dict):
            raise serializers.ValidationError(
                {'budget': "Бюджет должен быть в формате JSON-объекта."})

        for transaction_type in ['income', 'expense']:
            if transaction_type in budget_data:
                for category, category_data in budget_data[transaction_type].items():
                    if 'forecast' not in category_data or 'actual' not in category_data:
                        raise serializers.ValidationError(
                            {'budget': (
                                f"Категория {category} должна "
                                f"содержать 'forecast' и 'actual'."
                            )})
                    if not isinstance(category_data['forecast'], (int, float)) or not isinstance(
                            category_data['actual'], (int, float)):
                        raise serializers.ValidationError({
                            'budget': (
                                f"Значения 'forecast' и 'actual' "
                                f"в категории {category} должны быть числовыми."
                            )})

        return attrs
