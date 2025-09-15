import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import SubscriptionPlan, Subscription, Feature

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
    def post(self, request, *args, **kwargs):
        plan_id = self.kwargs["plan_id"]
        plan = SubscriptionPlan.objects.get(id=plan_id)
        
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'brl',
                            'product_data': {
                                'name': plan.title,
                            },
                            'unit_amount': int(plan.price * 100),
                            'recurring': {'interval': 'month'},
                        },
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url='http://127.0.0.1:8000/subscription/success/',
                cancel_url='http://127.0.0.1:8000/subscription/cancel/',
                metadata={
                    "plan_id": str(plan.id),
                    "user_id": str(request.user.id)
                }
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


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        user_id = session['metadata']['user_id']
        plan_id = session['metadata']['plan_id']
        
        plan = SubscriptionPlan.objects.get(id=plan_id)
        
        Subscription.objects.create(
            user_id=user_id,
            plan=plan,
            stripe_customer_id=session.customer,
            stripe_subscription_id=session.subscription,
            active=True
        )

    return HttpResponse(status=200)
