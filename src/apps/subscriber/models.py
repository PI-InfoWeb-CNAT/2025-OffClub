from django.db import models
from apps.core.services.validators import ValidatorService
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.coupon.models import Coupon
import uuid

class Subscriber(models.Model):
    _cpf_validator = ValidatorService.is_valid_cpf
    
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="subscriber",
        verbose_name="Usuário",
        primary_key=True
    )
    first_name = models.CharField("Nome", max_length=50, blank=False, null=False)
    last_name = models.CharField("Sobrenome", max_length=50, blank=False, null=False)
    cpf = models.CharField(
        "CPF",
        max_length=14,  # Formato: XXX.XXX.XXX-XX
        unique=True,
        validators=[_cpf_validator],
        blank=False,
        null=False
    )
    birth_date = models.DateField("Data de Nascimento", blank=True, null=True)
    # Identificador do cliente no Stripe (gateway de pagamento)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    
    active_subscription = models.OneToOneField(
        "subscription.Subscription",
        on_delete=models.SET_NULL, 
        related_name="active_for_subscriber",
        verbose_name="Assinatura Ativa",
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = "Assinante"
        verbose_name_plural = "Assinantes"
        ordering = ["user__email"]
        
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para garantir que o CPF seja salvo sem formatação.
        """
        self.cpf = self.cpf.replace(".", "").replace("-", "")
        super().save(*args, **kwargs)
        
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Evaluation(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False)
    stars = models.IntegerField("Estrelas", null=False,validators=[MaxValueValidator(5), MinValueValidator(1)])
    message = models.CharField("Mensagem", max_length=300)
    coupon = models.OneToOneField(
        Coupon, 
        related_name="evaluation",
        verbose_name="Cupom",
        on_delete=models.CASCADE
        )
    
    def __str__(self):
        return f"{self.coupon} - {self.stars} estrelas"

    class Meta:
        verbose_name = "Avaliação de Cupom"
        verbose_name_plural = "Avaliações de Cupons"
        ordering = ["coupon", "-stars"]
