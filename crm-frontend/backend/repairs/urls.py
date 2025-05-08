from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CarTypeListCreateView,
    CarTypeDetailView,
    CarPartViewSet,
    RepairStartView,
    RepairFinishView,
    RepairListCreateView,
    RepairDetailView,
    RepairDeleteView,
    CarListCreateView,
    CarDetailView,
)

router = DefaultRouter()
router.register(r'carparts', CarPartViewSet, basename='carpart')

urlpatterns = [
    path('', CarListCreateView.as_view(), name='car_list_create'),
    path('<int:id>/', CarDetailView.as_view(), name='car_detail'),
    path('cartypes/', CarTypeListCreateView.as_view(), name='car_type_list_create'),
    path('cartypes/<int:id>/', CarTypeDetailView.as_view(), name='car_type_detail'),
    path('', include(router.urls)),
    path('repair/start/', RepairStartView.as_view(), name='repair-start'),
    path('repair/finish/', RepairFinishView.as_view(), name='repair-finish'),
    path('repair/', RepairListCreateView.as_view(), name='repair-list-create'),
    path('repair/<int:id>/', RepairDetailView.as_view(), name='repair-detail'),
    path('repair/delete/<int:pk>/', RepairDeleteView.as_view(), name='repair-delete'),
]
