from rest_framework import serializers
from .models import Budget

class BudgetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'start_date', 'end_date']

class BudgetDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
