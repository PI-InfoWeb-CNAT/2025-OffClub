import os
import sys
import django
from datetime import timedelta
from decimal import Decimal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from django.utils import timezone
from django.db import transaction
from django.db.models import F

from apps.enterprise.models import LineOfBusiness, Enterprise
from apps.users.models import User
from apps.offer.models import Category, Offer
from apps.subscriber.models import Subscriber


def create_users_and_enterprises():
    lob_names = ['Alimentação', 'Beleza', 'Lazer', 'Saúde', 'Entretenimento']
    lobs = {}
    for name in lob_names:
        obj, _ = LineOfBusiness.objects.get_or_create(name=name)
        lobs[name] = obj
    # Criar pelo menos 5 empresas
    enterprises_data = [
        ('pizza_house@example.com', 'Pizza House LTDA', 'Pizza House', '12345678000195', 'Alimentação'),
        ('spa_relax@example.com', 'Spa Relax EIRELI', 'Spa Relax', '22345678000195', 'Beleza'),
        ('cine_top@example.com', 'Cine Top SA', 'Cine Top', '32345678000195', 'Entretenimento'),
        ('health_plus@example.com', 'Health Plus Ltda', 'Health Plus', '42345678000195', 'Saúde'),
        ('bistro_urban@example.com', 'Bistrô Urban ME', 'Bistrô Urban', '52345678000195', 'Alimentação'),
    ]

    enterprises = []
    for idx, (email, corp, trade, cnpj, lob_name) in enumerate(enterprises_data):
        password = f'pass{1000 + idx}'
        user, created = User.objects.get_or_create(email=email, defaults={'is_active': True, 'user_role': User.UserRole.ENTERPRISE})
        if created:
            user.set_password(password)
            user.save()

        ent, _ = Enterprise.objects.get_or_create(
            user=user,
            defaults={
                'corporate_reason': corp,
                'trade_name': trade,
                'cnpj': cnpj,
                'line_of_business': lobs.get(lob_name),
            }
        )
        enterprises.append(ent)

    return enterprises


def create_subscribers():
    subs_data = [
        {'email': 'ana@example.com', 'password': 'pass1234', 'first_name': 'Ana', 'last_name': 'Silva', 'cpf': '11122233344'},
        {'email': 'bruno@example.com', 'password': 'pass1234', 'first_name': 'Bruno', 'last_name': 'Pereira', 'cpf': '22233344455'},
        {'email': 'carla@example.com', 'password': 'pass1234', 'first_name': 'Carla', 'last_name': 'Souza', 'cpf': '33344455566'},
    ]

    subs = []
    for s in subs_data:
        user, created = User.objects.get_or_create(email=s['email'], defaults={'is_active': True, 'user_role': User.UserRole.SUBSCRIBER})
        if created:
            user.set_password(s['password'])
            user.save()

        sub, _ = Subscriber.objects.get_or_create(
            user=user,
            defaults={'first_name': s['first_name'], 'last_name': s['last_name'], 'cpf': s['cpf']}
        )
        subs.append(sub)

    return subs


def create_categories():
    names = ['Restaurante', 'Spa', 'Cinema', 'Beleza', 'Saúde']
    cats = []
    for n in names:
        c, _ = Category.objects.get_or_create(name=n)
        cats.append(c)
    return cats


def create_offers(enterprises, categories):
    now = timezone.now()
    # Gerar 25 ofertas distribuídas entre empresas e categorias
    offers = []
    total = 25
    for i in range(total):
        ent = enterprises[i % len(enterprises)]
        cat = categories[i % len(categories)]
        title = f'Oferta #{i+1} - {ent.trade_name}'
        description = f'Descrição da oferta {i+1} do estabelecimento {ent.trade_name}.'
        price = Decimal(f'{20 + (i % 10) * 5}.00')
        discount = (i * 7) % 60  # variação de desconto
        start = now - timedelta(days=(i % 3))
        end = start + timedelta(days=30 + (i % 10))
        max_coupons = 50

        offer, _ = Offer.objects.get_or_create(
            enterprise=ent,
            title=title,
            defaults={
                'description': description,
                'category': cat,
                'price': price,
                'discount': discount,
                'start_date': start,
                'end_date': end,
                'max_coupons': max_coupons,
            }
        )
        offers.append(offer)

    return offers


def generate_coupons(offers, subscribers):
    created = 0
    for offer in offers:
        for sub in subscribers:
            with transaction.atomic():
                off = Offer.objects.select_for_update().get(pk=offer.pk)

                # não criar mais cupons que o máximo
                if off.generated_coupons >= off.max_coupons:
                    break

                # evita duplicar cupons (unique_together subscriber+offer)
                if Coupon.objects.filter(offer=off, subscriber=sub).exists():
                    continue

                # calcula expiration_date explicitamente para evitar NOT NULL
                expiration = timezone.now() + off.redemption_period
                code = f"{off.title[:3].upper()}-{sub.user.email.split('@')[0].upper()}-{off.generated_coupons + 1}"

                coupon = Coupon.objects.create(code=code, subscriber=sub, offer=off, expiration_date=expiration)

                # atualizar contador de forma segura
                Offer.objects.filter(pk=off.pk).update(generated_coupons=F('generated_coupons') + 1)
                created += 1

    return created


if __name__ == '__main__':
    print('Iniciando seed de ofertas completo (empresas, categorias, ofertas)...')
    with transaction.atomic():
        enterprises = create_users_and_enterprises()
        # mantém criação de assinantes opcional para testes, mas não geramos cupons aqui
        _ = create_subscribers()
        categories = create_categories()
        offers = create_offers(enterprises, categories)

    print('\nResumo:')
    print(f'  Empresas criadas/obtidas: {len(enterprises)}')
    print(f'  Assinantes criados/obtidos: {len(Subscriber.objects.all())}')
    print(f'  Categorias criadas/obtidas: {len(categories)}')
    print(f'  Ofertas criadas/obtidas: {len(offers)}')
    print('Não foram gerados cupons — fluxo separado deverá criar cupons em execução.')
    print('Seed de ofertas concluído.')
