from rest_framework import generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .models import CarType, Car, CarPart
from .serializers import CarTypeSerializer, CarSerializer, CarPartSerializer


class CarTypeListCreateView(generics.ListCreateAPIView):
    queryset = CarType.objects.all()
    serializer_class = CarTypeSerializer


class CarTypeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CarType.objects.all()
    serializer_class = CarTypeSerializer
    lookup_field = 'id'


class CarListCreateView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = 'id'


class CarPartListCreateView(generics.ListCreateAPIView):
    queryset = CarPart.objects.all()
    serializer_class = CarPartSerializer


class CarPartDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CarPart.objects.all()
    serializer_class = CarPartSerializer
    lookup_field = 'id'
