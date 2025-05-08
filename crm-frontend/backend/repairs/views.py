from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action

from django.core.exceptions import ValidationError

from .models import CarType, Car, CarPart, Repair, Budget
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


class CarPartViewSet(viewsets.ModelViewSet):
    queryset = CarPart.objects.all()
    serializer_class = CarPartSerializer

    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        part = self.get_object()
        quantity = request.data.get('quantity')

        if not quantity:
            return Response(
                {"detail": "Quantity is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response(
                    {"detail": "Quantity must be positive"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {"detail": "Invalid quantity value"},
                status=status.HTTP_400_BAD_REQUEST
            )

        budget = Budget.objects.first()
        if not budget:
            return Response(
                {"detail": "Budget not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        total_cost = part.price * quantity

        if budget.value < total_cost:
            return Response(
                {"detail": "Not enough budget to purchase parts"},
                status=status.HTTP_400_BAD_REQUEST
            )

        part.in_stock += quantity
        part.save()

        budget.value -= total_cost
        budget.save()

        return Response({
            "detail": "Parts purchased successfully",
            "new_stock": part.in_stock,
            "remaining_budget": budget.value
        })


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


class RepairDeleteView(DestroyAPIView):
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer

    def perform_destroy(self, instance):
        car = instance.car
        car.state = car.CarState.NO_SERVICE
        car.save()

        instance.delete()


class RepairListCreateView(ListCreateAPIView):
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer


class RepairDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer
    lookup_field = 'id'