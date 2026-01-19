from django.db import models
from django.utils import timezone 
import uuid

class Coupon(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField("Código", max_length=7, unique=True)
    subscriber = models.ForeignKey("subscriber.Subscriber", on_delete=models.CASCADE, related_name="coupons", verbose_name="Assinante")
    offer = models.ForeignKey("offer.Offer", on_delete=models.CASCADE, related_name="coupons", verbose_name="Oferta")
    
    creation_date = models.DateTimeField("Data de Resgate", auto_now_add=True)
    expiration_date = models.DateTimeField("Data de Expiração do Cupom", null=True, blank=True)
    used_date = models.DateTimeField("Data de Uso", null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        # Gera código alfanumérico em maiúsculas com 7 caracteres, garantindo unicidade
        if not self.code:
            import random
            import string
            chars = string.ascii_uppercase + string.digits
            code = ''.join(random.choices(chars, k=7))
            # garante unicidade
            while Coupon.objects.filter(code=code).exists():
                code = ''.join(random.choices(chars, k=7))
            self.code = code

        # Mantém sempre em maiúsculas caso alguém passe um código manualmente
        self.code = (self.code or '').upper()

        if not self.expiration_date:
            # define expiration_date baseado no período de resgate da oferta
            try:
                self.expiration_date = timezone.now() + self.offer.redemption_period
            except Exception:
                # fallback seguro
                self.expiration_date = timezone.now()
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
