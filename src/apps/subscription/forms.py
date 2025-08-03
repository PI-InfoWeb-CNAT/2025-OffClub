from django import forms
from datetime import timedelta
from .models import SubscriptionPlan

class SubscriptionPlanForm(forms.ModelForm):
    duration_in_days = forms.IntegerField(
        label='Duração em dias',
        help_text='Digite a duração do plano em dias (ex: 30, 90, 365).'
    )

    class Meta:
        model = SubscriptionPlan
        fields = [
            'title', 'description', 'price', 'features'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.duration:
            self.fields['duration_in_days'].initial = self.instance.duration.days

    def save(self, commit=True):
        days = self.cleaned_data.get('duration_in_days')
        if days:
            self.instance.duration = timedelta(days=days)
        
        return super().save(commit=commit)