from django import forms 
from .models import Enterprise, LineOfBusiness
from apps.core.models import Address, Phone 
from apps.users.models import User  

# Forms pra registro de Empresa

class EnterpriseInfoForm(forms.ModelForm):
    line_of_business = forms.ModelChoiceField(
        queryset=LineOfBusiness.objects.all(),
        empty_label=None, 
        label="Ramo de Atividade", 
        widget=forms.RadioSelect 
    )
    class Meta:
        model = Enterprise
        fields = ['corporate_reason', 'trade_name', 'cnpj', 'line_of_business', 'description']
        widgets = {
            'corporate_reason': forms.TextInput(attrs={'placeholder': 'Razão Social'}),
            'trade_name': forms.TextInput(attrs={'placeholder': 'Nome Fantasia'}),
            'cnpj': forms.TextInput(attrs={'placeholder': 'CNPJ'}),
            'description': forms.Textarea(attrs={'placeholder': 'Descrição'}),
        }
        
class CredentialsForm(forms.ModelForm):
    password2 = forms.CharField(
        label="Confirme a Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme a Senha'}))
    
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Senha'}),
        }
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError("As senhas não coincidem.")
        return cd.get('password2')
    

class ContactForm(forms.Form):
    #Campos para o modelo Phone
    phone_number = forms.CharField(label="Telefone 1", max_length=15, help_text="(XX) XXXXX-XXXX")
    phone_number2 = forms.CharField(label="Telefone 2", max_length=15, required=False)

    # Campos para o modelo Address
    cep = forms.CharField(label="CEP", max_length=9)
    city = forms.CharField(label="Cidade", max_length=75)
    state = forms.CharField(label="UF", max_length=2)
    street_name = forms.CharField(label="Logradouro", max_length=75)
    number = forms.CharField(label="Número", max_length=10)
    complement = forms.CharField(label="Complemento", max_length=75, required=False)
    neighborhood = forms.CharField(label="Bairro", max_length=75)
    

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['profile_picture']
        
        
# Form de login 

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'E-mail'
                }
            )
        )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Senha'
            }
        )
    )