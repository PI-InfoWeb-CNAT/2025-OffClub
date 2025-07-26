from django.urls import path, include
from .views import SubscriptionPlanView

urlpatterns = [
    path('plans/', SubscriptionPlanView.as_view(), name='plans'),
]