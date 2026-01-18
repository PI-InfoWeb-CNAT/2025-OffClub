from django.db import models
from django.utils import timezone 
import uuid

class Coupon(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField("Código", max_length=100)
    subscriber = models.ForeignKey("subscriber.Subscriber", on_delete=models.CASCADE, related_name="coupons", verbose_name="Assinante")
    offer = models.ForeignKey("offer.Offer", on_delete=models.CASCADE, related_name="coupons", verbose_name="Oferta")
    
    creation_date = models.DateTimeField("Data de Resgate", auto_now_add=True)
    expiration_date = models.DateTimeField("Data de Expiração do Cupom")
    used_date = models.DateTimeField("Data de Uso", null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiration_date = timezone.now() + self.offer.redemption_period
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        if self.used_date:
            return False
        return timezone.now() <= self.expiration_date

    @property
    def days_left(self):        
        delta = self.expiration_date - timezone.now()
        return max(delta.days, 0)

    def __str__(self):
        return f"{self.offer.title} - {self.subscriber.first_name}"

    class Meta:
        verbose_name = "Cupom"
        verbose_name_plural = "Cupons"
        ordering = ["-creation_date"]
        unique_together = ("subscriber", "offer")
