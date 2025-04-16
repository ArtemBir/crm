from rest_framework import serializers

from .models import CarType, Car, CarPart, CarState


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    state = serializers.ChoiceField(choices=CarState.choices)

    class Meta:
        model = Car
        fields = '__all__'


class CarPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarPart
        fields = '__all__'
