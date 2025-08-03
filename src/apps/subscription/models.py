from django.db import models
import uuid

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
    active = models.BooleanField('Ativo', default=True)

    def __str__(self):
        return f'{self.user} - {self.plan.title}'

    class Meta:
        verbose_name = 'Assinatura'
        verbose_name_plural = 'Assinaturas'
        ordering = ['-start_date']
        
        