from django import forms 
from .models import Subscriber 
from apps.core.models import Address, Phone 
from apps.users.models import User  

# Forms pra registro de assinante

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['first_name', 'last_name', 'cpf', 'birth_date']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nome', 'class': 'half-width'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Sobrenome', 'class': 'half-width'}),
            'cpf': forms.TextInput(attrs={'placeholder': 'CPF', 'class': 'half-width'}),
            'birth_date': forms.DateInput(attrs={'placeholder': 'Data de Nascimento', 'type': 'date', 'class': 'half-width'}),
        }
        
class CredentialsForm(forms.ModelForm):
    password2 = forms.CharField(label="Confirme a Senha", widget=forms.PasswordInput(attrs={'placeholder': 'Confirme a Senha', 'class': 'half-width'}))
    
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Senha', 'class': 'half-width'}),
        }
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError("As senhas não coincidem.")
        return cd.get('password2')
    

class ContactForm(forms.ModelForm):
    phone_number = forms.CharField(label="Telefone 1", max_length=15, help_text="(XX) XXXXX-XXXX", widget=forms.TextInput(attrs={'placeholder': 'Telefone 1', 'class': 'half-width'}))
    phone_number2 = forms.CharField(label="Telefone 2", max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Telefone 2', 'class': 'half-width'}))
    cep = forms.CharField(label="CEP", max_length=9, widget=forms.TextInput(attrs={'placeholder': 'CEP', 'class': 'third-width'}))
    city = forms.CharField(label="Cidade", max_length=75, widget=forms.TextInput(attrs={'placeholder': 'Cidade', 'class': 'third-width'}))
    state = forms.CharField(label="UF", max_length=2, widget=forms.TextInput(attrs={'placeholder': 'UF',  'class': 'third-width'}))
    street_name = forms.CharField(label="Logradouro", max_length=75, widget=forms.TextInput(attrs={'placeholder': 'Logradouro', 'class': 'half-width'}))
    number = forms.CharField(label="Número", max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Número', 'class': 'half-width'}))
    complement = forms.CharField(label="Complemento", max_length=75, required=False, widget=forms.TextInput(attrs={'placeholder': 'Complemento', 'class': 'half-width'}))
    neighborhood = forms.CharField(label="Bairro", max_length=75, widget=forms.TextInput(attrs={'placeholder': 'Bairro', 'class': 'half-width'}))
    
    class Meta:
        model = Subscriber 
        fields = []  # Não é usado campos do modelo Subscriber diretamente aqui
    

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['profile_picture']
        
        
# Form de login 

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'E-mail'
                }
            )
        )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Senha'
            }
        )
    )
    
    
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta: 
        model = Review
        fields = ["stars", "message"]
        widgets = {
            "stars": forms.HiddenInput(),   # o valor vai vir do JS
            "message": forms.Textarea(attrs={"rows": 3, "placeholder": "Conte um pouco da sua experiência"})
        }