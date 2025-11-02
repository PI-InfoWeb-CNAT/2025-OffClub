from django.db import transaction
from apps.enterprise.models import Enterprise 
from apps.users.models import User 

class EnterpriseRequestService:
    @staticmethod
    @transaction.atomic # Garante que a operação no banco ou falhe ou tenha sucesso
    def approve(enterprise: Enterprise):
        if not enterprise.user:
            raise ValueError(f"Empresa {enterprise.pk} não possui um usuário associado.")
            
        user = enterprise.user
        user.is_active = True
        user.save(update_fields=['is_active'])

    @staticmethod
    @transaction.atomic
    def deny(enterprise: Enterprise):
        if not enterprise.user:
            raise ValueError(f"Empresa {enterprise.pk} não possui um usuário associado.")
        user = enterprise.user
        user.delete()