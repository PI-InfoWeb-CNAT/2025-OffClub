from django.db import models
from .services.validators import ValidatorService
import uuid
import re


class Phone(models.Model):
    class PhoneType(models.TextChoices):
        MOBILE = "Mobile", "Celular"
        LANDLINE = "Landline", "Fixo"
        WHATSAPP = "WhatsApp", "WhatsApp"
        OTHER = "Other", "Outro"
    
    _phone_validator = ValidatorService.is_valid_phone
    
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='phones', 
        null=True, 
        blank=True
    )
    phone_number = models.CharField("Número de Telefone", null=False, max_length=15, validators=[_phone_validator])
    phone_type = models.CharField("Tipo de Telefone", max_length=20, choices=PhoneType.choices, default=PhoneType.MOBILE)
    
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para garantir que o número de telefone seja salvo sem formatação.
        """
        self.phone_number = self.phone_number.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        super().save(*args, **kwargs)
    
    def _get_formatted_number(self):
        """
        Formata o número de telefone para o padrão (XX) XXXXX-XXXX.
        """
        if len(self.phone_number) == 11:
            return f"({self.phone_number[:2]}) {self.phone_number[2:7]}-{self.phone_number[7:]}"
        
        if len(self.phone_number) == 10:
            return f"({self.phone_number[:2]}) {self.phone_number[2:6]}-{self.phone_number[6:]}"
        
        return self.phone_number

    def __str__(self):
        return f'{self._get_formatted_number()}'

    class Meta:
        verbose_name = 'Telefone'
        verbose_name_plural = 'Telefones'
        ordering = ['phone_number']
        unique_together = ('phone_number', 'phone_type')
    

class Address(models.Model):
    class State(models.TextChoices):
        AC = "AC", "Acre"
        AL = "AL", "Alagoas"
        AP = "AP", "Amapá"
        AM = "AM", "Amazonas"
        BA = "BA", "Bahia"
        CE = "CE", "Ceará"
        DF = "DF", "Distrito Federal"
        ES = "ES", "Espírito Santo"
        GO = "GO", "Goiás"
        MA = "MA", "Maranhão"
        MT = "MT", "Mato Grosso"
        MS = "MS", "Mato Grosso do Sul"
        MG = "MG", "Minas Gerais"
        PA = "PA", "Pará"
        PB = "PB", "Paraíba"
        PR = "PR", "Paraná"
        PE = "PE", "Pernambuco"
        PI = "PI", "Piauí"
        RJ = "RJ", "Rio de Janeiro"
        RN = "RN", "Rio Grande do Norte"
        RS = "RS", "Rio Grande do Sul"
        RO = "RO", "Rondônia"
        RR = "RR", "Roraima"
        SC = "SC", "Santa Catarina"
        SP = "SP", "São Paulo"
        SE = "SE", "Sergipe"
        TO = "TO", "Tocantins"
        
    _cep_validator = ValidatorService.is_valid_cep
    
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='addresses', 
        null=True, 
        blank=True
    )
    cep = models.CharField("CEP", null=False, max_length=9, validators=[_cep_validator])
    state = models.CharField("Estado", max_length=2, choices=State.choices, default=State.RN)
    city = models.CharField("Cidade", null=False, max_length=75)
    neighborhood = models.CharField("Bairro", null=False, max_length=75)
    street_name = models.CharField("Nome da Rua", null=False, max_length=75)
    number = models.CharField("Número", null=False, max_length=5)
    complement = models.CharField("Complemento", blank=True, null=True, max_length=75)
    
    def save(self, *args, **kwargs):
        # Armazena apenas os dígitos para consistência
        self.cep = re.sub(r'\D', '', self.cep)
        super().save(*args, **kwargs)

    @property
    def formatted_cep(self):
        """Formata o CEP para exibição."""
        cep_str = str(self.cep)
        if len(cep_str) == 8:
            return f"{cep_str[:5]}-{cep_str[5:]}"
        return self.cep

    def __str__(self):
        return f'{self.street_name}, {self.number} - {self.neighborhood}, {self.city} - {self.state} ({self.cep})'
    
    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        ordering = ['street_name', 'number']

