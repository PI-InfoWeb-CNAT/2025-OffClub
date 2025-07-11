from django.urls import path, include
from .views import historico

urlpatterns = [
    path('historico_consumo', historico, name='historico')
]