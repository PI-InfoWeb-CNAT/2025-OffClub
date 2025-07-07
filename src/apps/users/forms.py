from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    """
    Um formulário para criar novos usuários sem o campo username.
    """
    class Meta(UserCreationForm.Meta): 
        model = User
        fields = ('email', 'user_role') 

class CustomUserChangeForm(UserChangeForm):
    """
    Um formulário para atualizar usuários sem o campo username.
    """
    class Meta:
        model = User
        fields = ('email', 'user_role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')