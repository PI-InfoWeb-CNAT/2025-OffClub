from django import forms
from ..models import Offer

# formulário de criar ofertas pelas empresas
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
