from django.db import models
import uuid
from django.utils import timezone

class Feature(models.Model):
    name = models.CharField('Nome', max_length=100, unique=True)
    description = models.TextField('Descrição', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Feature'
        verbose_name_plural = 'Features'
        ordering = ['name']


class SubscriptionPlan(models.Model):
    id = models.UUIDField("ID",primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Título', null=False, max_length=100)
    description = models.CharField('Descrição', null=False, max_length=400)
    price = models.DecimalField('Preço', max_digits=5, decimal_places=2)
    duration = models.DurationField('Duração em dias', null=False)
    features = models.ManyToManyField(Feature, related_name='plans', blank=True)
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f'{self.title} - {self.duration} dias'

    class Meta:
        verbose_name = 'Plano de Assinatura'
        verbose_name_plural = 'Planos de Assinatura'
        ordering = ['title']


class Subscription(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='subscriptions') 
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, related_name='subscriptions', null=True, blank=True)
    start_date = models.DateTimeField('Data de Início', auto_now_add=True)
    end_date = models.DateTimeField('Data de Término', null=True, blank=True)
    @property
    def is_active(self):
        """
        Verifica dinamicamente se a assinatura está dentro do período de validade.
        """
        now = timezone.now()
        if not self.end_date: # Assinaturas sem data de fim podem ser consideradas ativas
             return self.start_date <= now
        return self.start_date <= now <= self.end_date

    # Identificador da assinatura no Stripe (gateway de pagamento)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)
    
    def cancel(self):
        """
        Cancela a assinatura imediatamente definindo a `end_date` para o momento atual.
        Retorna True se a assinatura foi cancelada; False se já estava inativa.
        """
        if not self.is_active:
            return False
        self.end_date = timezone.now()
        self.save(update_fields=["end_date"])
        return True

    def __str__(self):
        return f'{self.user} - {self.plan.title if self.plan else "Sem Plano"}'

    class Meta:
        verbose_name = 'Assinatura'
        verbose_name_plural = 'Assinaturas'
        ordering = ['-start_date']
