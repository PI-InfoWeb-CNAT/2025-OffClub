from django.db import models
from django.utils import timezone 
from django.core.validators import MinValueValidator, MaxValueValidator
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

    def __str__(self):
        return f"{self.offer.title} - {self.subscriber.first_name}"

    class Meta:
        verbose_name = "Cupom"
        verbose_name_plural = "Cupons"
        ordering = ["-creation_date"]
        unique_together = ("subscriber", "offer")


class Evaluation(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False)
    stars = models.IntegerField("Estrelas", null=False,validators=[MaxValueValidator(5), MinValueValidator(1)])
    message = models.CharField("Mensagem", max_length=300)
    coupon = models.ForeignKey(
        Coupon, 
        related_name="evaluations",
        verbose_name="Cupom",
        on_delete=models.CASCADE
        )
    
    def __str__(self):
        return f"{self.coupon} - {self.stars} estrelas"

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        ordering = ["coupon", "-stars"]
        unique_together = ("coupon",)