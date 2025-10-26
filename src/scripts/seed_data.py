


import os, sys, django
from datetime import timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.subscription.models import Feature, SubscriptionPlan

# DADOS DE INSERÇÃO
features_data = [
    {'name': 'Acesso Premium', 'description': 'Acesso a conteúdos exclusivos.'},
    {'name': 'Suporte Prioritário', 'description': 'Atendimento prioritário ao cliente.'},
    {'name': 'Descontos Especiais', 'description': 'Descontos em produtos e serviços.'},
    {'name': 'Conteúdo Offline', 'description': 'Acesso a conteúdos para visualização offline.'},
    {'name': 'Múltiplos Dispositivos', 'description': 'Acesso em vários dispositivos simultaneamente.'},
]

plans_data = [
    {
        'title': 'Plano Básico',
        'description': 'Acesso limitado ao conteúdo.',
        'price': 29.90,
        'duration': timedelta(days=30),
        'stripe_price_id': 'price_basic_001',
        'features': [0], # índices dos features
    },
    {
        'title': 'Plano Premium',
        'description': 'Acesso total ao conteúdo e suporte.',
        'price': 59.90,
        'duration': timedelta(days=30),
        'stripe_price_id': 'price_premium_001',
        'features': [0, 1, 2, 3, 4],
    },
    {
        'title': 'Plano Família',
        'description': 'Acesso para até 5 membros da família.',
        'price': 89.90,
        'duration': timedelta(days=30),
        'stripe_price_id': 'price_family_001',
        'features': [0, 1, 2, 4],
    },
    {
        'title': 'Plano Empresarial',
        'description': 'Soluções personalizadas para empresas.',
        'price': 199.90,
        'duration': timedelta(days=30),
        'stripe_price_id': 'price_business_001',
        'features': [0, 1, 2, 3, 4],
    }
]

# PROCESSO DE INSERÇÃO NO BANCO
features_objs = []
for f in features_data:
    obj, _ = Feature.objects.get_or_create(**f)
    features_objs.append(obj)

for p in plans_data:
    plan, _ = SubscriptionPlan.objects.get_or_create(
        title=p['title'],
        description=p['description'],
        price=p['price'],
        duration=p['duration'],
        stripe_price_id=p['stripe_price_id'],
    )
    plan.features.set([features_objs[i] for i in p['features']])

print('Seed concluído.')
