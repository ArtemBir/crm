from rest_framework import generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .models import Car
from .serializers import CarSerializer


class CarListCreateView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class CarDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = 'id'