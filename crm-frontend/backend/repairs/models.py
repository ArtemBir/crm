from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal

from src.app.accounting.models import Budget
from src.app.customers.models import Customer


class CarType(models.Model):
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.make} {self.model}'


class CarPart(models.Model):
    name = models.CharField(max_length=100)
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE, null=True, blank=True, related_name='parts')
    price = models.PositiveIntegerField(default=0)
    in_stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Car(models.Model):
    class CarState(models.TextChoices):
        IN_SERVICE = 'IN_SERVICE', 'In Service'
        NO_SERVICE = 'NO_SERVICE', 'No Service'

    year = models.PositiveIntegerField()
    color = models.CharField(max_length=30)
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE, null=True, blank=True, related_name='cars')
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, related_name='cars')
    state = models.CharField(max_length=20, choices=CarState.choices, default=CarState.NO_SERVICE)

    def __str__(self):
        customer_info = (f'Customer ID: {self.customer.id}' if self.customer else 'No customer')
        state_display = self.get_state_display()
        return f'({self.car_type}) {self.year} {self.color} ({state_display}) {customer_info}'

    def repair_start(self, car_part: CarPart):
        if not car_part.in_stock:
            raise ValidationError(f"Car part {car_part.name} is not in storage.")

        if not self.customer:
            raise ValidationError('Car has no owner assigned.')

        if self.customer.budget < car_part.price:
            raise ValidationError('Customer does not have enough budget.')

        self.customer.budget -= car_part.price
        self.customer.save()

        repair, created = Repair.objects.get_or_create(car=self)
        if created:
            repair.customer = self.customer
        repair.car_parts.add(car_part)
        repair.expense += Decimal(str(car_part.price)) * Decimal('1.1')
        repair.save()

        if car_part.in_stock <= 0:
            raise ValidationError(f"Car part {car_part.name} is out of stock.")

        car_part.in_stock = car_part.in_stock - 1
        car_part.save()

        self.state = self.CarState.IN_SERVICE
        self.save()

    def repair_finish(self, car_part: CarPart):

        repair = Repair.objects.filter(car=self).first()
        if not repair:
            raise ValueError(f"No repair found for car {self.id}")

        self.state = self.CarState.NO_SERVICE
        self.save()


class Repair(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='repairs')
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE, related_name='repairs')
    car_parts = models.ManyToManyField(CarPart, related_name='repairs')
    expense = models.DecimalField(default=0, decimal_places=1, max_digits=10)

    def price(self):
        total = sum(part.price for part in self.car_parts.all())
        return int(total * 1.1)
