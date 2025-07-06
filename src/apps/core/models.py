from django.db import models
from ..auth_user.models import AuthUser

# Create your models here.
class Phone(models.Model):
    class PhoneType(models.TextChoices):
        FIXO = 'Fixo'
        MOVEL = 'Móvel'
    auth_user = models.ForeignKey(AuthUser, null=True, on_delete=models.SET_NULL)
    number = models.CharField(null=False, max_length=13)
    type = models.CharField(choices=PhoneType)
    main_number = models.BooleanField()

    def __str__(self):
        return '{}'.format(self.number)