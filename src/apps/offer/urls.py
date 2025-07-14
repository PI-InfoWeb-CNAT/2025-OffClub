from django.urls import path, include
from .views import OfferViews
from . import views

urlpatterns = [
    path('detalharoferta/', views.offer, name='offer_detail'),
    path('', OfferViews.list_filter_offer)
]
