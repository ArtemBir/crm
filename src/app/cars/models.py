from django.db import models

# Create your models here.
class Car(models.Model):
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    year = models.IntegerField()
    color = models.CharField(max_length=30)

