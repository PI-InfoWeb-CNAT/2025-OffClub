from django.urls import path, include
from .views import EvaluationCreateView

app_name = "coupon"

urlpatterns = [
    path('avaliar_cupom/', EvaluationCreateView.as_view(), name='evaluate_coupon'),
]