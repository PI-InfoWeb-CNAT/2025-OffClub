from django.db import models
from ..subscriber.models import Subscriber
from ..offer.models import Offer

# Create your models here.
class Coupon(models.Model):
    subscriber = models.OneToOneField(Subscriber, on_delete=models.SET_NULL, null=True)
    offer = models.OneToOneField(Offer, on_delete=models.SET_NULL, null=True)
    code = models.CharField(null=False, max_length=100)
    creation_date = models.DateTimeField(null=False, auto_now_add=True)
    expiration_date = models.DateTimeField(null=False)
    active = models.BooleanField()
    def __str__(self):
        return '{}'.format(self.code)