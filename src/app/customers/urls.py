from django.urls import path
from .views import CustomerListCreateView, CustomerDetailView

urlpatterns = [
    path('', CustomerListCreateView.as_view()),
    path('/<int:id>', CustomerDetailView.as_view()),
]
