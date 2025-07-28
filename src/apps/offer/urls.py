from django.urls import path, include
from .views import OfferViews

urlpatterns = [
    path('', OfferViews.offer, name='offer_list')
]
