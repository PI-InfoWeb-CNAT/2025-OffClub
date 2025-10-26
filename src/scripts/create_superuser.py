import os, sys, django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()


from django.contrib.auth import get_user_model
User = get_user_model()

admin_email = 'admin@example.com'
admin_password = 'admin'

if not User.objects.filter(email=admin_email).exists():
    User.objects.create_superuser(
        email=admin_email,
        password=admin_password,
        user_role=User.UserRole.ADMIN,
        is_approved=True
    )
    print('Superusuário admin criado com sucesso!')
else:
    print('Superusuário admin já existe.')
