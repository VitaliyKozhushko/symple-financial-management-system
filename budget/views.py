from rest_framework import generics
from .models import Budget
from .serializers import BudgetListSerializer, BudgetDetailSerializer
from .celery_tasks import check_budget_limit

class BudgetListView(generics.ListAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetListSerializer

class BudgetDetailView(generics.RetrieveAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetDetailSerializer

class BudgetCreateView(generics.CreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetDetailSerializer

    def perform_create(self, serializer):
        budget = serializer.save()
        check_budget_limit.delay(budget.id)

class BudgetUpdateView(generics.UpdateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetDetailSerializer

class BudgetDeleteView(generics.DestroyAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetDetailSerializer
