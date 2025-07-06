from django.db import models
from ..coupon.models import Coupon

# Create your models here.
class Review(models.Model):
    coupon = models.ForeignKey(Coupon, null=True, on_delete=models.SET_NULL)
    creation_date = models.DateField(auto_now_add=True)
    stars = models.IntegerField(null=False)
    message = models.CharField(null=False, max_length=325)

    def __str__(self):
        return '{}'.format(self.stars)