from rest_framework import serializers

from src.app.customers.models import Customer
from src.app.tech.serializers import CarSerializer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'

    cars = CarSerializer(many=True, read_only=True)