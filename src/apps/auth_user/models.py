from django.db import models
from django.contrib.auth.models import User
from ..enterprise.models import Enterprise

# Create your models here.

class AuthUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enterprise = models.OneToOneField(Enterprise, blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(blank=True, null=True)
    cep = models.CharField(null=False, max_length=9)
    state = models.CharField(null=False, max_length=2)
    city = models.CharField(null=False, max_length=50)
    neighborhood = models.CharField(null=False, max_length=50)
    street_name = models.CharField(null=False, max_length=50)
    number = models.CharField(null=False, max_length=5)
    address_complement = models.CharField(blank=True, null=True, max_length=50)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'