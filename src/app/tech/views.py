from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from .models import CarType, Car, CarPart, Repair
from .serializers import CarTypeSerializer, CarSerializer, CarPartSerializer, RepairSerializer


class CarTypeListCreateView(ListCreateAPIView):
    queryset = CarType.objects.all()
    serializer_class = CarTypeSerializer


class CarTypeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CarType.objects.all()
    serializer_class = CarTypeSerializer
    lookup_field = 'id'


class CarListCreateView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = 'id'


class CarPartListCreateView(ListCreateAPIView):
    queryset = CarPart.objects.all()
    serializer_class = CarPartSerializer


class CarPartDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CarPart.objects.all()
    serializer_class = CarPartSerializer
    lookup_field = 'id'


class RepairStartView(APIView):
    def post(self, request):
        car_id = request.data.get('car_id')
        part_id = request.data.get('car_part_id')

        try:
            car = Car.objects.get(id=car_id)
            part = CarPart.objects.get(id=part_id)
            car.repair_start(part)
            return Response({'message': f'Repair started for car {car_id} with part {part_id}.'})
        except (Car.DoesNotExist, CarPart.DoesNotExist):
            return Response({'error': 'Car or Part not found.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RepairFinishView(APIView):
    def post(self, request):
        car_id = request.data.get('car_id')
        part_id = request.data.get('car_part_id')

        try:
            car = Car.objects.get(id=car_id)
            part = CarPart.objects.get(id=part_id)
            car.repair_finish(part)
            return Response({'message': f'Repair finished for car {car_id} with part {part_id}.'})
        except (Car.DoesNotExist, CarPart.DoesNotExist):
            return Response({'error': 'Car or Part not found.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RepairListCreateView(ListCreateAPIView):
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer


class RepairDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer
    lookup_field = 'id'
