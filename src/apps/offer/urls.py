from django.urls import path, include
from . import views

urlpatterns = [
    path('detalharoferta/', views.offer, name='offer_detail')
]