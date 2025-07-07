from django.db import models
from apps.core.services.validators import ValidatorService
import re

class LineOfBusiness(models.Model):
    """
    Entidade que representa os ramos que uma empresa atua.
    """
    name = models.CharField("Nome do ramo", max_length=100, unique=True)
    
    class Meta:
        verbose_name = "Ramo de Atividade"
        verbose_name_plural = "Ramos de Atividade"
        ordering = ['name']

    def __str__(self):
        return self.name
    

class Enterprise(models.Model):
    _cnpj_validator = ValidatorService.is_valid_cnpj
    
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="enterprise",
        verbose_name="Usuário",
        primary_key=True
    )
    corporate_reason = models.CharField("Razão Social", max_length=200, unique=True)
    trade_name = models.CharField("Nome Fantasia", max_length=200, blank=False, null=False)
    description = models.TextField("Descrição", max_length=500, blank=True, null=True)
    cnpj = models.CharField(
        "CNPJ",
        max_length=18,  # Formato: XX.XXX.XXX/XXXX-XX
        unique=True,
        validators=[_cnpj_validator],
        blank=False,
        null=False
    )
    line_of_business = models.ForeignKey(
        LineOfBusiness,
        on_delete=models.SET_NULL,
        related_name="enterprises",
        verbose_name="Ramo de Atividade",
        null=True,
        blank=True
    )
    
    def save(self, *args, **kwargs):
        """Garante que o CNPJ seja salvo apenas com dígitos."""
        if self.cnpj:
            self.cnpj = re.sub(r'\D', '', self.cnpj)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.trade_name} | ({self.corporate_reason})"
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["trade_name"]
    
