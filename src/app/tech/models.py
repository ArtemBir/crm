from django.db import models

from src.app.customers.models import Customer


class CarType(models.Model):
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.make} {self.model}'


class Car(models.Model):
    class CarState(models.TextChoices):
        IN_SERVICE = 'IN_SERVICE', 'In Service'
        NO_SERVICE = 'NO_SERVICE', 'No Service'

    year = models.PositiveIntegerField()
    color = models.CharField(max_length=30)
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE, null=True, blank=True, related_name='cars')
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, related_name='cars')
    state = models.CharField(max_length=20, choices=CarState.choices, default=CarState.IN_SERVICE)

    def __str__(self):
        customer_info = (f'Customer ID: {self.customer.id}' if self.customer else 'No customer')
        state_display = self.get_state_display()
        return f'({self.car_type}) {self.year} {self.color} ({state_display}) {customer_info}'


class CarPart(models.Model):
    name = models.CharField(max_length=100)
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE, null=True, blank=True, related_name='parts')

    def __str__(self):
        return self.name
