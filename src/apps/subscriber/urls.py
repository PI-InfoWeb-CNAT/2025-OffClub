from django.urls import path, include
from .views import SubscriberViews

urlpatterns = [
    path('historico_consumo/', SubscriberViews.historico, name='historico')
]