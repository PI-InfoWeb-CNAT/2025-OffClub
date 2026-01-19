from django.test import TestCase
from django.utils import timezone
from apps.users.models import User
from .models import SubscriptionPlan, Subscription


class SubscriptionCancelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', is_active=True)
        self.plan = SubscriptionPlan.objects.create(title='Teste', description='desc', price=10.0, duration=timezone.timedelta(days=30))
        self.sub = Subscription.objects.create(user=self.user, plan=self.plan)

    def test_cancel_sets_end_date_and_deactivates(self):
        self.assertTrue(self.sub.is_active)
        canceled = self.sub.cancel()
        self.assertTrue(canceled)
        self.sub.refresh_from_db()
        self.assertIsNotNone(self.sub.end_date)
        self.assertFalse(self.sub.is_active)
