from django.urls import path

from .views import (
    CarTypeListCreateView,
    CarTypeDetailView,
    CarListCreateView,
    CarDetailView,
    CarPartListCreateView,
    CarPartDetailView,
)

urlpatterns = [
    path('cartypes/', CarTypeListCreateView.as_view(), name='car_type_list_create'),
    path('cartypes/<int:id>/', CarTypeDetailView.as_view(), name='car_type_detail'),
    path('', CarListCreateView.as_view(), name='car_list_create'),
    path('<int:id>/', CarDetailView.as_view(), name='car_detail'),
    path('carparts/', CarPartListCreateView.as_view(), name='car_part_list_create'),
    path('carparts/<int:id>/', CarPartDetailView.as_view(), name='car_part_detail'),
]
