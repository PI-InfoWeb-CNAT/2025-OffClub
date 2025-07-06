from django.db import models
from ..auth_user.models import AuthUser
from ..subscription_plan.models import SubscriptionPlan

# Create your models here.

class Subscriber(models.Model):
    user = models.OneToOneField(AuthUser, null=False, on_delete=models.CASCADE)
    cpf = models.CharField(null=False, max_length=11)
    birth_date = models.DateField(null=False)

    def __str__(self):
        return f"{self.user.user.first_name} {self.user.user.last_name}"

class Subscription(models.Model):
    subscriber = models.OneToOneField(Subscriber, null=True, on_delete=models.CASCADE)
    subscription_plan = models.OneToOneField(SubscriptionPlan, null=True, on_delete=models.CASCADE)
    start_date = models.DateField(null=False, auto_now_add=True)
    end_date = models.DateField(null=False)
    active = models.BooleanField(null=False)

    def __str__(self):
        return f'{SubscriptionPlan} - {Subscriber}'