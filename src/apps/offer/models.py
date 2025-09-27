from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import timedelta
import uuid
from django import forms  # <--- precisa importar

class Category(models.Model):
    name = models.CharField("Nome", max_length=50, unique=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Offer(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False)
    enterprise = models.ForeignKey(
        "enterprise.Enterprise",
        on_delete=models.CASCADE,
        related_name="offers",
        verbose_name="Empresa",
    )
    title = models.CharField("Título", max_length=100)
    description = models.TextField("Descrição", max_length=500)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="offers",
        verbose_name="Categoria",
        null=True,
        blank=True,
    )
    image = models.ImageField("Imagem", upload_to="uploads/offers/", null=True, blank=True)
    price = models.DecimalField("Preço", max_digits=10, decimal_places=2)
    discount = models.PositiveSmallIntegerField(
        "Desconto (%)",
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    start_date = models.DateTimeField("Data de Início", default=timezone.now)
    end_date = models.DateTimeField("Data de Expiração")
    redemption_period = models.DurationField("Período de Resgate", default=timedelta(days=30))
    max_coupons = models.IntegerField("Quantidade máxima", default=1, validators=[MinValueValidator(1)])
    generated_coupons = models.IntegerField("Cupons gerados", default=0)

    @property
    def final_price(self):
        if not self.price:
            return 0
        return self.price - (self.price * self.discount / 100)

    @property
    def discount_value(self):
        return self.price * self.discount / 100

    @property
    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def to_dict(self):
        remaining_coupons = self.max_coupons - self.generated_coupons
        return {
            "id": str(self.id),
            "title": self.title,
            "image_url": self.image.url if self.image else None,
            "description": self.description,
            "discount": self.discount,
            "price": f"{self.price:.2f}".replace(".", ","),
            "final_price": f"{self.final_price:.2f}".replace(".", ","),
            "discount_value": f"{self.discount_value:.2f}".replace(".", ","),
            "start_date": self.start_date.strftime("%d/%m/%Y"),
            "end_date": self.end_date.strftime("%d/%m/%Y"),
            "redemption_period_days": self.redemption_period.days,
            "remaining_coupons": remaining_coupons,
            "max_coupons": self.max_coupons,
            "enterprise": {
                "trade_name": self.enterprise.trade_name,
                "logo_url": (
                    self.enterprise.user.profile_picture.url
                    if getattr(self.enterprise.user, "profile_picture", None)
                    else None
                ),
            },
            "category": {"name": self.category.name if self.category else "Sem Categoria"},
        }

    def clean(self):
        super().clean()
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "A data final deve ser posterior à data inicial."})
        if self.generated_coupons > self.max_coupons:
            raise ValidationError(
                {"generated_coupons": "A oferta está esgotada e todos os cupons foram resgatados."}
            )

    def __str__(self):
        return f"{self.title} - {self.enterprise.trade_name}"

    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"
        ordering = ["-start_date"]
        constraints = [
            models.UniqueConstraint(fields=["title", "enterprise"], name="uniq_enterprise_title")
        ]


# Formulário de criar ofertas pelas empresas
class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            "enterprise", "title", "description", "category",
            "image", "price", "discount",
            "start_date", "end_date", "redemption_period",
            "max_coupons"
        ]
        widgets = {
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
