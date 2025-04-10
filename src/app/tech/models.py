from django.db import models

from src.app.customers.models import Customer


class CarType(models.Model):
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.make} {self.model}'


class Car(models.Model):
    year = models.IntegerField()
    color = models.CharField(max_length=30)
    car_type = models.ForeignKey(
        CarType, on_delete=models.CASCADE, null=True, blank=True, related_name='cars'
    )
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL, related_name='cars'
    )

    def __str__(self):
        customer_info = (
            f'Customer ID: {self.customer.id}' if self.customer else 'No customer'
        )
        return f'{self.year} {self.color} ({self.car_type}) {customer_info}'


class CarPart(models.Model):
    name = models.CharField(max_length=100)
    car_type = models.ForeignKey(
        CarType, on_delete=models.CASCADE, null=True, blank=True, related_name='parts'
    )

    def __str__(self):
        return self.name
