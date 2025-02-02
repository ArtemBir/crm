from django.db import models

from src.app.customers.models import Customer


class Car(models.Model):
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    year = models.IntegerField()
    color = models.CharField(max_length=30)
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL, related_name="cars"
    )

    def __str__(self):
        customer_info = f"Customer ID: {self.customer.id}" if self.customer else "No customer"
        return f"{self.make} {self.model} ({self.year}) {self.color} {customer_info}"
