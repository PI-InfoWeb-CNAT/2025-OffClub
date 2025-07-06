from django.db import models
from ..enterprise.models import Enterprise

# Create your models here.
class Category(models.Model):
    name = models.CharField(null=False, max_length=25)

    def __str__(self):
        return '{}'.format(self.name)

class Offer(models.Model):
    enterprise = models.OneToOneField(Enterprise, null=True, on_delete=models.SET_NULL)
    categories = models.ManyToManyField(Category)
    name = models.CharField(null=False, max_length=100)
    description = models.CharField(null=False, max_length=300)
    start_date = models.DateTimeField(null=False, auto_now_add=True)
    end_date = models.DateTimeField(null=False)
    expiration = models.IntegerField()
    max_qtd = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)