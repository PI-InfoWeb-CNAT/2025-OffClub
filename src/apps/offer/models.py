from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta 
import uuid

class Category(models.Model):
    name = models.CharField("Nome", max_length=50, unique=True)
    
    class Meta: 
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Offer(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False)
    enterprise = models.ForeignKey("enterprise.Enterprise", on_delete=models.CASCADE, related_name="offers", verbose_name="Empresa")
    title = models.CharField("Título", max_length=100)
    description = models.TextField("Descrição", max_length=500)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="offers", verbose_name="Categoria", null=True, blank=True)
    image = models.ImageField("Imagem", upload_to="uploads/offers/", null=True, blank=True)
    price = models.DecimalField("Preço", max_digits=10, decimal_places=2)
    discount = models.PositiveSmallIntegerField("Desconto (%)", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    start_date = models.DateTimeField("Data de Início", default=timezone.now)
    end_date = models.DateTimeField("Data de Expiração")
    redemption_period = models.DurationField("Período de Resgate", default=timedelta(days=30))
    
    @property
    def is_active(self):
        return self.start_date <= timezone.now() <= self.end_date
    
    def __str__(self):
        return f"{self.title} - {self.enterprise.trade_name}"
    
    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"
        ordering = ['-start_date']
        unique_together = ('title', 'enterprise')