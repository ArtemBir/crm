from django.urls import path
from .views import BudgetListCreateView, BudgetDetailView

urlpatterns = [
    path('budget/', BudgetListCreateView.as_view(), name='budget-list-create'),
    path('budget/<int:id>/', BudgetDetailView.as_view(), name='budget-detail'),
]