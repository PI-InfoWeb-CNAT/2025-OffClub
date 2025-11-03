from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid 
from apps.core.services.validators import ValidatorService 

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O e-mail deve ser fornecido.")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class UserRole(models.TextChoices):
        ADMIN = 'Admin', 'Administrador'
        SUBSCRIBER = 'Subscriber', 'Assinante'
        ENTERPRISE = 'Enterprise', 'Empresa'

    _email_validator = ValidatorService.is_valid_email
    
    # Telefone e Endereço estão relacionados no modelo Address e Phone,
    # então não é necessário ter campos separados aqui.
    
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False)
    profile_picture = models.ImageField("Foto de Perfil", upload_to='uploads/profile_pics/', blank=True, null=True, default="static/imgs/default-profile-picture.png")
    user_role = models.CharField("Papel do Usuário", max_length=20, choices=UserRole.choices, default=UserRole.SUBSCRIBER)
    email = models.EmailField("E-mail", unique=True, validators=[_email_validator], blank=False, null=False)
    date_joined = models.DateTimeField("Data de Registro", auto_now_add=True)
    
    is_active = models.BooleanField("Ativo", default=True)
    is_staff = models.BooleanField("Equipe", default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['-date_joined']