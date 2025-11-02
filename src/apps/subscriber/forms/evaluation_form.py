from django import forms
from ..models import Evaluation

class EvaluationForm(forms.ModelForm):
    class Meta: 
        model = Evaluation
        fields = ["stars", "message"]
        widgets = {
            "stars": forms.HiddenInput(),   # o valor vai vir do JS
            "message": forms.Textarea(attrs={"rows": 3, "placeholder": "Conte um pouco da sua experiência"})
        }
    