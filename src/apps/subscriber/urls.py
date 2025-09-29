from django.urls import path, include
from .views import SubscriberViews

urlpatterns = [
    path('historico_consumo/', SubscriberViews.consumption_history_list, name='history')
]