from django.db import models

class Budget(models.Model):
    value = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Budget: {self.value}'
