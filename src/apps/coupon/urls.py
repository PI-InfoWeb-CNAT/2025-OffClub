from django.urls import path, include
from .views import EvaluationCreateView

app_name = "coupon"

urlpatterns = [
    path('avaliar_cupom/<uuid:coupon_id>/', EvaluationCreateView.as_view(), name='evaluate_coupon'),
]