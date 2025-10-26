from datetime import timedelta
import stripe
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import SubscriptionPlan, Subscription, Feature
from apps.users.models import User 

stripe.api_key = settings.STRIPE_SECRET_KEY

class SubscriptionPlanView(View):
    template_name = 'plans.html'

    def get(self, request):
        plans = SubscriptionPlan.objects.all().prefetch_related('features').order_by('price')
        all_features = Feature.objects.all()

        context = {
            'plans': plans,
            'all_features': all_features,
            'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
        }

        return render(request, self.template_name, context)


class CreateCheckoutSessionView(View):
    def post(self, request, plan_id):
        if not request.user.is_authenticated:
            return redirect('subscriber:login')
        plan = SubscriptionPlan.objects.get(id=plan_id)
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
                end_date=timezone.now() + timedelta(days=30)
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return JsonResponse({'error': str(e)})


class SuccessView(View):
    def get(self, request):
        return render(request, 'success.html')

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
