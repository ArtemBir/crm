from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .models import Budget
from .serializers import BudgetSerializer

class BudgetListCreateView(ListCreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

class BudgetDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    lookup_field = 'id'