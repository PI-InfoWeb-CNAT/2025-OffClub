from django.urls import path, include
from .views import SubscriberViews, EvaluationCreateView

app_name = "subscriber"

urlpatterns = [
    path('historico_consumo/', SubscriberViews.consumption_history_list, name='history'),
    path('avaliar_cupom/<uuid:coupon_id>/', EvaluationCreateView.as_view(), name='evaluate_coupon'),
]