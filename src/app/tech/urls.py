from django.urls import path

from .views import (
    CarTypeListCreateView,
    CarTypeDetailView,
    CarListCreateView,
    CarDetailView,
    CarPartListCreateView,
    CarPartDetailView,
    RepairStartView,
    RepairFinishView,
    RepairListCreateView,
    RepairDetailView
)

urlpatterns = [
    path('cartypes/', CarTypeListCreateView.as_view(), name='car_type_list_create'),
    path('cartypes/<int:id>/', CarTypeDetailView.as_view(), name='car_type_detail'),
    path('', CarListCreateView.as_view(), name='car_list_create'),
    path('<int:id>/', CarDetailView.as_view(), name='car_detail'),
    path('carparts/', CarPartListCreateView.as_view(), name='car_part_list_create'),
    path('carparts/<int:id>/', CarPartDetailView.as_view(), name='car_part_detail'),
    path('repair/start/', RepairStartView.as_view(), name='repair-start'),
    path('repair/finish/', RepairFinishView.as_view(), name='repair-finish'),
    path('repair/', RepairListCreateView.as_view(), name='repair-list-create'),
    path('repair/<int:id>/', RepairDetailView.as_view(), name='repair-detail'),
]
