from django.urls import path

from .views import CarDetailView, CarListCreateView

urlpatterns = [
    path('', CarListCreateView.as_view()),
    path('<int:id>', CarDetailView.as_view()),
]
