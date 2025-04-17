from rest_framework import serializers

from .models import CarType, Car, CarPart


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    state = serializers.CharField(source='get_state_display', read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'car_type', 'year', 'color', 'state']


class CarPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarPart
        fields = '__all__'
