from datetime import timedelta
import stripe
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import SubscriptionPlan, Subscription, Feature

stripe.api_key = settings.STRIPE_SECRET_KEY

class SubscriptionPlanView(View):
    template_name = 'plans.html'

    def get(self, request):
        plans = SubscriptionPlan.objects.all().prefetch_related('features').order_by('price')
        all_features = Feature.objects.all()
        active_subscription = self._get_active_subscription(request.user)
        subscription_error = request.session.pop('subscription_error', None)

        context = {
            'plans': plans,
            'all_features': all_features,
            'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
            'active_subscription': active_subscription,
            'subscription_error': subscription_error,
        }

        return render(request, self.template_name, context)

    @staticmethod
    def _get_active_subscription(user):
        if not user.is_authenticated:
            return None

        now = timezone.now()
        return (
            Subscription.objects
            .filter(user=user, start_date__lte=now)
            .filter(Q(end_date__gte=now) | Q(end_date__isnull=True))
            .select_related('plan')
            .order_by('-start_date')
            .first()
        )


class CreateCheckoutSessionView(View):
    def post(self, request, plan_id):
        if not request.user.is_authenticated:
            return redirect('subscriber:login')
        plan = get_object_or_404(SubscriptionPlan, id=plan_id)

        active_subscription = SubscriptionPlanView._get_active_subscription(request.user)
        if active_subscription:
            request.session['subscription_error'] = (
                f"Você já possui uma assinatura ativa do plano "
                f"{active_subscription.plan.title if active_subscription.plan else 'atual'}"
            )
            return redirect('subscription:plans')

        if not plan.stripe_price_id:
            request.session['subscription_error'] = 'Plano temporariamente indisponível para pagamento online.'
            return redirect('subscription:plans')

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': plan.stripe_price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=request.build_absolute_uri('/subscription/success/'),
                cancel_url=request.build_absolute_uri('/subscription/cancel/'),
                metadata={
                    "plan_id": str(plan.id),
                    "user_id": str(request.user.id)
                }
            )
            # Registra a assinatura localmente (stripe não consegue acessar o webhook)
            Subscription.objects.create(
                user=request.user,
                plan=plan,
                end_date=timezone.now() + (plan.duration or timedelta(days=30))
            )
            return redirect(checkout_session.url)
        except Exception as e:
            request.session['subscription_error'] = 'Não foi possível iniciar o checkout. Tente novamente em instantes.'
            return redirect('subscription:plans')


class SuccessView(View):
    def get(self, request):
        active_subscription = SubscriptionPlanView._get_active_subscription(request.user)
        return render(request, 'success.html', {'active_subscription': active_subscription})

class CancelView(View):
    def get(self, request):
        return render(request, 'cancel.html')



from django.utils.decorators import method_decorator

# @method_decorator(csrf_exempt, name='dispatch')
# class StripeWebhookView(View):
#     def post(self, request, *args, **kwargs):
#         payload = request.body
#         sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
#         event = None

#         try:
#             event = stripe.Webhook.construct_event(
#                 payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#             )
#         except ValueError:
#             return HttpResponse(status=400)
#         except stripe.error.SignatureVerificationError:
#             return HttpResponse(status=400)

#         print(f"Evento recebido: {event['type']}")
#         if event['type'] == 'checkout.session.completed':
#             session = event['data']['object']
#             user_id = session['metadata']['user_id']
#             plan_id = session['metadata']['plan_id']
#             plan = SubscriptionPlan.objects.get(id=plan_id)
#             try:
#                 print("AAAAAAAAAAAAAAAAAAAAAAAAAA")
#                 from apps.users.models import User
#                 user = User.objects.get(id=user_id)
#                 Subscription.objects.create(
#                     user=user,
#                     plan=plan,
#                     stripe_customer_id=session.get('customer'),
#                     stripe_subscription_id=session.get('subscription'),
#                     active=True
#                 )
#             except Exception as e:
#                 print(f'Erro ao criar assinatura: {e}')
#         return HttpResponse(status=200)
