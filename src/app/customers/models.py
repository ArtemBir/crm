from django.db import models


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name} {self.phone}'
