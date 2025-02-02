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

