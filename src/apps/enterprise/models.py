from django.db import models

# Create your models here.
class OperationArea(models.Model):
    name = models.CharField(null=False, max_length=30)

    def __str__(self):
        return '{}'.format(self.name)
    

class Enterprise (models.Model):
    operation_areas = models.ManyToManyField(OperationArea)
    trade_name = models.CharField(null=False, max_length=50)
    corporate_reason = models.CharField(null=False, max_length=50)
    description = models.CharField(null=False, max_length=200)
    cnpj = models.CharField(null=False, max_length=14)
    cep = models.CharField(null=False, max_length=9)
    state = models.CharField(null=False, max_length=2)
    city = models.CharField(null=False, max_length=50)
    neighborhood = models.CharField(null=False, max_length=50)
    street_name = models.CharField(null=False, max_length=50)
    number = models.CharField(null=False, max_length=5)
    address_complement = models.CharField(blank=True, null=True, max_length=50)

    def __str__(self):
        return '{}'.format(self.trade_name)
    
