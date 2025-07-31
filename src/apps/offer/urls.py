from django.urls import path, include
from .views import OfferViews

urlpatterns = [
    path('detalhar_oferta/', OfferViews.offer, name='offer_detail'),
    path('', OfferViews.list_filter_offer)
]
