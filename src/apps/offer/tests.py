from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from apps.offer.models import Offer
from apps.users.models import User
from apps.subscriber.models import Subscriber
from datetime import timedelta

class RedeemOfferTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Usuário assinante
        self.user = User.objects.create_user(email='user@example.com', password='secret')
        self.subscriber = Subscriber.objects.create(user=self.user, first_name='Test', last_name='User', cpf='12345678901')

        # Criar uma oferta válida
        now = timezone.now()
        self.offer = Offer.objects.create(
            enterprise=self._create_enterprise(),
            title='Oferta Teste',
            description='desc',
            price=100,
            discount=10,
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=10),
            max_coupons=2,
            generated_coupons=0,
        )

    def _create_enterprise(self):
        from apps.enterprise.models import Enterprise
        from apps.users.models import User
        u = User.objects.create_user(email='ent@example.com', password='secret', user_role=User.UserRole.ENTERPRISE)
        return Enterprise.objects.create(user=u, trade_name='Loja')

    def test_redeem_creates_coupon_and_decrements(self):
        self.client.login(email='user@example.com', password='secret')
        url = reverse('offer:redeem', args=[str(self.offer.id)])
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data.get('success'))
        coupon = data.get('coupon')
        self.assertIsNotNone(coupon)
        self.assertEqual(len(coupon['code']), 7)
        self.assertTrue(coupon['code'].isupper())
        # expiration_date deve estar presente e ser uma string ISO
        self.assertIn('expiration_date', coupon)
        self.assertIsNotNone(coupon['expiration_date'])

        # também confirma que o registro foi persistido e tem expiration_date
        from apps.coupon.models import Coupon as CouponModel
        db_coupon = CouponModel.objects.get(id=coupon['id'])
        self.assertIsNotNone(db_coupon.expiration_date)

        self.offer.refresh_from_db()
        self.assertEqual(self.offer.generated_coupons, 1)

    def test_cannot_redeem_twice_same_user(self):
        self.client.login(email='user@example.com', password='secret')
        url = reverse('offer:redeem', args=[str(self.offer.id)])
        self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)

    def test_offer_exhaustion(self):
        # Redeem with two different users until exhausted
        self.client.login(email='user@example.com', password='secret')
        url = reverse('offer:redeem', args=[str(self.offer.id)])
        self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Segundo usuário
        user2 = User.objects.create_user(email='user2@example.com', password='secret')
        Subscriber.objects.create(user=user2, first_name='Other', last_name='User', cpf='98765432100')
        self.client.logout()
        self.client.login(email='user2@example.com', password='secret')
        self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Agora oferta deve estar esgotada
        user3 = User.objects.create_user(email='user3@example.com', password='secret')
        Subscriber.objects.create(user=user3, first_name='Third', last_name='User', cpf='11122233344')
        self.client.logout()
        self.client.login(email='user3@example.com', password='secret')
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
