


import os, sys, django
from datetime import timedelta
from decimal import Decimal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from django.utils import timezone
from apps.subscription.models import Feature, SubscriptionPlan
from apps.offer.models import Category, Offer
from apps.enterprise.models import Enterprise, LineOfBusiness
from apps.users.models import User

# ========================================
# DADOS DE FEATURES E PLANOS
# ========================================
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
        'stripe_price_id': 'price_1SMVZ0DsNernzDNXYLt1sBig',
        'features': [0],
    },
    {
        'title': 'Plano Premium',
        'description': 'Acesso total ao conteúdo e suporte.',
        'price': 59.90,
        'duration': timedelta(days=30),
        'stripe_price_id': 'price_1SMVRTDsNernzDNX6uZMtcCn',    
        'features': [0, 1, 2, 3, 4],
    },
    {
        'title': 'Plano Família',
        'description': 'Acesso para até 5 membros da família.',
        'price': 89.90,
        'duration': timedelta(days=30),
        'stripe_price_id': 'price_1SMVZVDsNernzDNXuUZiJBO2',
        'features': [0, 1, 2, 4],
    },
]

# ========================================
# DADOS DE CATEGORIAS
# ========================================
categories_data = [
    'Alimentação',
    'Tecnologia',
    'Moda',
    'Saúde e Beleza',
    'Esportes',
    'Entretenimento',
    'Educação',
    'Casa e Decoração',
    'Automotivo',
    'Viagens',
]

# ========================================
# DADOS DE RAMOS DE ATIVIDADE
# ========================================
lines_of_business_data = [
    'Restaurante',
    'Loja de Eletrônicos',
    'Loja de Roupas',
    'Salão de Beleza',
    'Academia',
    'Cinema',
    'Escola de Idiomas',
    'Loja de Móveis',
    'Oficina Mecânica',
    'Agência de Viagens',
]

# ========================================
# DADOS DE EMPRESAS (para criar ofertas)
# ========================================
enterprises_data = [
    {
        'email': 'contato@pizzariabella.com',
        'corporate_reason': 'Pizzaria Bella Napoli LTDA',
        'trade_name': 'Pizzaria Bella Napoli',
        'description': 'A melhor pizza artesanal da cidade, com ingredientes frescos e massa feita na hora.',
        'cnpj': '12345678000101',
        'line_of_business': 'Restaurante',
    },
    {
        'email': 'vendas@tecnomax.com',
        'corporate_reason': 'TecnoMax Eletrônicos LTDA',
        'trade_name': 'TecnoMax',
        'description': 'Sua loja de eletrônicos com os melhores preços e garantia estendida.',
        'cnpj': '23456789000102',
        'line_of_business': 'Loja de Eletrônicos',
    },
    {
        'email': 'contato@modastyle.com',
        'corporate_reason': 'Moda Style Confecções LTDA',
        'trade_name': 'Moda Style',
        'description': 'Roupas modernas e acessíveis para todas as ocasiões.',
        'cnpj': '34567890000103',
        'line_of_business': 'Loja de Roupas',
    },
    {
        'email': 'agendamento@beautycare.com',
        'corporate_reason': 'Beauty Care Estética LTDA',
        'trade_name': 'Beauty Care',
        'description': 'Salão de beleza completo com profissionais especializados.',
        'cnpj': '45678901000104',
        'line_of_business': 'Salão de Beleza',
    },
    {
        'email': 'contato@fitpower.com',
        'corporate_reason': 'Fit Power Academia LTDA',
        'trade_name': 'Fit Power Academia',
        'description': 'Academia completa com equipamentos modernos e personal trainers.',
        'cnpj': '56789012000105',
        'line_of_business': 'Academia',
    },
    {
        'email': 'contato@burguerking.com',
        'corporate_reason': 'Burger House Restaurante LTDA',
        'trade_name': 'Burger House',
        'description': 'Hambúrgueres artesanais com carnes selecionadas.',
        'cnpj': '67890123000106',
        'line_of_business': 'Restaurante',
    },
    {
        'email': 'matriculas@idiomaspro.com',
        'corporate_reason': 'Idiomas Pro Educação LTDA',
        'trade_name': 'Idiomas Pro',
        'description': 'Escola de idiomas com metodologia exclusiva e professores nativos.',
        'cnpj': '78901234000107',
        'line_of_business': 'Escola de Idiomas',
    },
    {
        'email': 'vendas@casanova.com',
        'corporate_reason': 'Casa Nova Móveis LTDA',
        'trade_name': 'Casa Nova Móveis',
        'description': 'Móveis de qualidade para deixar sua casa ainda mais bonita.',
        'cnpj': '89012345000108',
        'line_of_business': 'Loja de Móveis',
    },
]

# ========================================
# DADOS DE OFERTAS
# ========================================
offers_data = [
    {
        'title': 'Pizza Grande + Refrigerante 2L',
        'description': 'Escolha qualquer sabor de pizza grande e ganhe um refrigerante de 2 litros. Válido para consumo no local ou delivery.',
        'category': 'Alimentação',
        'price': Decimal('79.90'),
        'discount': 30,
        'days_valid': 45,
        'max_coupons': 100,
        'enterprise_index': 0,
    },
    {
        'title': 'Smartphone com 25% OFF',
        'description': 'Desconto especial em smartphones selecionados. Aproveite para trocar seu celular antigo!',
        'category': 'Tecnologia',
        'price': Decimal('1999.90'),
        'discount': 25,
        'days_valid': 30,
        'max_coupons': 50,
        'enterprise_index': 1,
    },
    {
        'title': 'Camiseta + Calça Jeans',
        'description': 'Compre uma camiseta e uma calça jeans com desconto exclusivo. Várias cores disponíveis.',
        'category': 'Moda',
        'price': Decimal('189.90'),
        'discount': 40,
        'days_valid': 60,
        'max_coupons': 200,
        'enterprise_index': 2,
    },
    {
        'title': 'Corte + Escova + Hidratação',
        'description': 'Pacote completo de beleza: corte, escova e hidratação profunda para seus cabelos.',
        'category': 'Saúde e Beleza',
        'price': Decimal('150.00'),
        'discount': 35,
        'days_valid': 30,
        'max_coupons': 80,
        'enterprise_index': 3,
    },
    {
        'title': 'Mensalidade Academia 50% OFF',
        'description': 'Primeira mensalidade com 50% de desconto. Inclui acesso a todas as modalidades.',
        'category': 'Esportes',
        'price': Decimal('99.90'),
        'discount': 50,
        'days_valid': 15,
        'max_coupons': 30,
        'enterprise_index': 4,
    },
    {
        'title': 'Combo Burger Duplo',
        'description': 'Hambúrguer duplo + batata grande + milk shake. O combo mais pedido da casa!',
        'category': 'Alimentação',
        'price': Decimal('54.90'),
        'discount': 20,
        'days_valid': 30,
        'max_coupons': 150,
        'enterprise_index': 5,
    },
    {
        'title': 'Curso de Inglês - 3 meses',
        'description': 'Curso intensivo de inglês por 3 meses com material incluso e certificado.',
        'category': 'Educação',
        'price': Decimal('899.00'),
        'discount': 45,
        'days_valid': 60,
        'max_coupons': 25,
        'enterprise_index': 6,
    },
    {
        'title': 'Sofá 3 Lugares Retrátil',
        'description': 'Sofá retrátil e reclinável em tecido suede. Conforto para toda a família.',
        'category': 'Casa e Decoração',
        'price': Decimal('2499.00'),
        'discount': 30,
        'days_valid': 45,
        'max_coupons': 15,
        'enterprise_index': 7,
    },
    {
        'title': 'Fone Bluetooth Premium',
        'description': 'Fone de ouvido bluetooth com cancelamento de ruído e bateria de 40h.',
        'category': 'Tecnologia',
        'price': Decimal('349.90'),
        'discount': 35,
        'days_valid': 30,
        'max_coupons': 100,
        'enterprise_index': 1,
    },
    {
        'title': 'Jaqueta de Couro Sintético',
        'description': 'Jaqueta estilosa em couro sintético. Disponível em preto e marrom.',
        'category': 'Moda',
        'price': Decimal('299.90'),
        'discount': 25,
        'days_valid': 45,
        'max_coupons': 60,
        'enterprise_index': 2,
    },
    {
        'title': 'Manicure + Pedicure + Esmaltação',
        'description': 'Serviço completo de unhas com esmaltação em gel ou tradicional.',
        'category': 'Saúde e Beleza',
        'price': Decimal('80.00'),
        'discount': 30,
        'days_valid': 30,
        'max_coupons': 120,
        'enterprise_index': 3,
    },
    {
        'title': 'Personal Trainer - 10 sessões',
        'description': 'Pacote de 10 sessões com personal trainer. Treino personalizado para seus objetivos.',
        'category': 'Esportes',
        'price': Decimal('500.00'),
        'discount': 40,
        'days_valid': 60,
        'max_coupons': 20,
        'enterprise_index': 4,
    },
    {
        'title': 'Rodízio de Pizza para 2',
        'description': 'Rodízio completo de pizzas para duas pessoas. Mais de 30 sabores disponíveis.',
        'category': 'Alimentação',
        'price': Decimal('109.80'),
        'discount': 25,
        'days_valid': 30,
        'max_coupons': 80,
        'enterprise_index': 0,
    },
    {
        'title': 'Smart TV 50" 4K',
        'description': 'Smart TV LED 50 polegadas com resolução 4K e sistema operacional integrado.',
        'category': 'Tecnologia',
        'price': Decimal('2799.00'),
        'discount': 20,
        'days_valid': 15,
        'max_coupons': 10,
        'enterprise_index': 1,
    },
    {
        'title': 'Mesa de Jantar 6 Lugares',
        'description': 'Mesa de jantar em madeira maciça com 6 cadeiras estofadas.',
        'category': 'Casa e Decoração',
        'price': Decimal('1899.00'),
        'discount': 35,
        'days_valid': 45,
        'max_coupons': 12,
        'enterprise_index': 7,
    },
    {
        'title': 'Curso de Espanhol - Básico',
        'description': 'Curso completo de espanhol básico com 6 meses de duração.',
        'category': 'Educação',
        'price': Decimal('1200.00'),
        'discount': 50,
        'days_valid': 30,
        'max_coupons': 30,
        'enterprise_index': 6,
    },
]

# ========================================
# PROCESSO DE INSERÇÃO
# ========================================

print('Iniciando seed de dados...')

# Inserir Features
features_objs = []
for f in features_data:
    obj, created = Feature.objects.get_or_create(**f)
    features_objs.append(obj)
    if created:
        print(f'  ✓ Feature criada: {obj.name}')

# Inserir Planos
for p in plans_data:
    plan, created = SubscriptionPlan.objects.get_or_create(
        title=p['title'],
        defaults={
            'description': p['description'],
            'price': p['price'],
            'duration': p['duration'],
            'stripe_price_id': p['stripe_price_id'],
        }
    )
    plan.features.set([features_objs[i] for i in p['features']])
    if created:
        print(f'  ✓ Plano criado: {plan.title}')

# Inserir Categorias
categories_objs = {}
for cat_name in categories_data:
    obj, created = Category.objects.get_or_create(name=cat_name)
    categories_objs[cat_name] = obj
    if created:
        print(f'  ✓ Categoria criada: {obj.name}')

# Inserir Ramos de Atividade
lines_objs = {}
for line_name in lines_of_business_data:
    obj, created = LineOfBusiness.objects.get_or_create(name=line_name)
    lines_objs[line_name] = obj
    if created:
        print(f'  ✓ Ramo criado: {obj.name}')

# Inserir Empresas
enterprises_objs = []
for ent in enterprises_data:
    # Criar usuário para a empresa
    user, user_created = User.objects.get_or_create(
        email=ent['email'],
        defaults={
            'is_active': True,
            'user_role': 'Enterprise',
        }
    )
    if user_created:
        user.set_password('senha123')
        user.save()
    
    # Criar empresa
    enterprise, ent_created = Enterprise.objects.get_or_create(
        user=user,
        defaults={
            'corporate_reason': ent['corporate_reason'],
            'trade_name': ent['trade_name'],
            'description': ent['description'],
            'cnpj': ent['cnpj'],
            'line_of_business': lines_objs.get(ent['line_of_business']),
        }
    )
    enterprises_objs.append(enterprise)
    if ent_created:
        print(f'  ✓ Empresa criada: {enterprise.trade_name}')

# Inserir Ofertas
for offer_data in offers_data:
    enterprise = enterprises_objs[offer_data['enterprise_index']]
    category = categories_objs.get(offer_data['category'])
    
    offer, created = Offer.objects.get_or_create(
        title=offer_data['title'],
        enterprise=enterprise,
        defaults={
            'description': offer_data['description'],
            'category': category,
            'price': offer_data['price'],
            'discount': offer_data['discount'],
            'start_date': timezone.now(),
            'end_date': timezone.now() + timedelta(days=offer_data['days_valid']),
            'max_coupons': offer_data['max_coupons'],
        }
    )
    if created:
        print(f'  ✓ Oferta criada: {offer.title} ({enterprise.trade_name})')

print('\n✅ Seed concluído com sucesso!')
