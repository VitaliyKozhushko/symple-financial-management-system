from rest_framework import generics
from .models import Budget
from .serializers import BudgetListSerializer, BudgetDetailSerializer
from .celery_tasks import check_budget_limit

class BudgetListView(generics.ListAPIView):  # type: ignore
    queryset = Budget.objects.all()
    serializer_class = BudgetListSerializer

class BudgetDetailView(generics.RetrieveAPIView):  # type: ignore
    queryset = Budget.objects.all()
    serializer_class = BudgetDetailSerializer

class BudgetCreateView(generics.CreateAPIView):  # type: ignore
    queryset = Budget.objects.all()
    serializer_class = BudgetDetailSerializer

    def perform_create(self, serializer):
        budget = serializer.save()
        check_budget_limit.delay(budget.id)

class BudgetUpdateView(generics.UpdateAPIView):  # type: ignore
    queryset = Budget.objects.all()
    serializer_class = BudgetDetailSerializer
    http_method_names = ['put']

    def perform_update(self, serializer):
        budget = serializer.save()
        check_budget_limit.delay(budget.id)

class BudgetDeleteView(generics.DestroyAPIView):  # type: ignore
    queryset = Budget.objects.all()
    serializer_class = BudgetDetailSerializer
