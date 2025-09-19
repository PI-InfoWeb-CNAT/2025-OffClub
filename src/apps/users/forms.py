from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User
from apps.subscriber.models import Subscriber
from apps.enterprise.models import Enterprise

class SubscriberSignUpForm(UserCreationForm):
    """
    Formulário de registro para Assinantes.
    Agora inclui campos do perfil Subscriber e cria ambas as instâncias.
    """
    first_name = forms.CharField(max_length=50, required=True, label="Nome")
    last_name = forms.CharField(max_length=50, required=True, label="Sobrenome")
    cpf = forms.CharField(max_length=14, required=True, label="CPF")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_role = User.UserRole.SUBSCRIBER
        user.is_active = True
        user.is_approved = True
        
        if commit:
            user.save()
            Subscriber.objects.create(
                user=user,
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                cpf=self.cleaned_data.get('cpf')
            )
        return user

class EnterpriseSignUpForm(UserCreationForm):
    """
    Formulário de registro para Empresas.
    Agora inclui campos do perfil Enterprise e cria ambas as instâncias.
    """
    trade_name = forms.CharField(max_length=200, required=True, label="Nome Fantasia")
    corporate_reason = forms.CharField(max_length=200, required=True, label="Razão Social")
    cnpj = forms.CharField(max_length=18, required=True, label="CNPJ")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_role = User.UserRole.ENTERPRISE
        user.is_active = False
        user.is_approved = False

        if commit:
            user.save()
            Enterprise.objects.create(
                user=user,
                trade_name=self.cleaned_data.get('trade_name'),
                corporate_reason=self.cleaned_data.get('corporate_reason'),
                cnpj=self.cleaned_data.get('cnpj')
            )
        return user
