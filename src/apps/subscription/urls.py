from django.urls import path
from .views import SubscriptionPlanView, CreateCheckoutSessionView, SuccessView, CancelView, stripe_webhook

urlpatterns = [
    path('plans/', SubscriptionPlanView.as_view(), name='plans'),
    path('create-checkout-session/<uuid:plan_id>/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('webhooks/stripe/', stripe_webhook, name='stripe_webhook'),
]
