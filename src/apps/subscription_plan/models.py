from django.db import models

# Create your models here.
class SubscriptionPlan(models.Model):
    name = models.CharField(null=False, max_length=75)
    description = models.CharField(null=False, max_length=400)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.DecimalField(max_digits=3, decimal_places=0)

    def __str__(self):
        return f'{self.name} - {self.duration} days'