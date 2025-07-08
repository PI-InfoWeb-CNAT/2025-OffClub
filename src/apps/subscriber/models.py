from django.db import models
from apps.core.services.validators import ValidatorService

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
    
    subscription = models.ManyToManyField(
        "subscription.Subscription",
        related_name="subscribers",
        verbose_name="Assinaturas",
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
