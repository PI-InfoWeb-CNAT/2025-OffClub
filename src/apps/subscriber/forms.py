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
            'first_name': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Sobrenome'}),
            'cpf': forms.TextInput(attrs={'placeholder': 'CPF'}),
            'birth_date': forms.DateInput(attrs={'placeholder': 'Data de Nascimento', 'type': 'date'}),
        }
        
class CredentialsForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirme a Senha'}))
    
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
    

class ContactForm(forms.ModelForm):
    phone_number = forms.CharField(label="Telefone 1", max_length=15)
    cep = forms.CharField(label="CEP", max_length=9)
    city = forms.CharField(label="Cidade", max_length=75)
    state = forms.CharField(label="UF", max_length=2)
    neighborhood = forms.CharField(label="Bairro", max_length=75)
    street_name = forms.CharField(label="Logradouro", max_length=75)
    number = forms.CharField(label="Número", max_length=5)
    complement = forms.CharField(label="Complemento", max_length=75, required=False)
    
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
    
    
from .models import Evaluation


class EvaluationForm(forms.ModelForm):
    class Meta: 
        model = Evaluation
        fields = ["stars", "message"]
        widgets = {
            "stars": forms.HiddenInput(),   # o valor vai vir do JS
            "message": forms.Textarea(attrs={"rows": 3, "placeholder": "Conte um pouco da sua experiência"})
        }


class EditProfileForm(forms.ModelForm):
    # User fields
    profile_picture = forms.ImageField(label="Foto de Perfil", required=False)

    # Phone fields
    phone_number = forms.CharField(label="Telefone", max_length=15, required=False)

    # Address fields
    cep = forms.CharField(label="CEP", max_length=9, required=False)
    city = forms.CharField(label="Cidade", max_length=75, required=False)
    state = forms.CharField(label="UF", max_length=2, required=False)
    neighborhood = forms.CharField(label="Bairro", max_length=75, required=False)
    street_name = forms.CharField(label="Logradouro", max_length=75, required=False)
    number = forms.CharField(label="Número", max_length=5, required=False)
    complement = forms.CharField(label="Complemento", max_length=75, required=False)

    class Meta:
        model = Subscriber
        fields = ['first_name', 'last_name', 'birth_date']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Sobrenome'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['profile_picture'].initial = user.profile_picture
            phone = user.phones.first()
            if phone:
                self.fields['phone_number'].initial = phone.phone_number
            address = user.addresses.first()
            if address:
                self.fields['cep'].initial = address.cep
                self.fields['city'].initial = address.city
                self.fields['state'].initial = address.state
                self.fields['neighborhood'].initial = address.neighborhood
                self.fields['street_name'].initial = address.street_name
                self.fields['number'].initial = address.number
                self.fields['complement'].initial = address.complement

    def save(self, commit=True):
        subscriber = super().save(commit=False)
        
        if commit:
            subscriber.save()
            
        user = subscriber.user
        
        # Save profile pic
        if self.cleaned_data.get('profile_picture'):
            user.profile_picture = self.cleaned_data['profile_picture']
            user.save()
        
        # Save Phone
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            phone = user.phones.first()
            if phone:
                phone.phone_number = phone_number
                phone.save()
            else:
                Phone.objects.create(user=user, phone_number=phone_number, phone_type=Phone.PhoneType.MOBILE)

        # Save Address
        address_data = {k: self.cleaned_data.get(k) for k in ['cep', 'city', 'state', 'neighborhood', 'street_name', 'number', 'complement']}
        
        if any(address_data.values()): 
             address = user.addresses.first()
             if address:
                 for key, value in address_data.items():
                     setattr(address, key, value)
                 address.save()
             else:
                 Address.objects.create(user=user, **address_data)
        
        return subscriber