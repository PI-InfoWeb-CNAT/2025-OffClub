from django.urls import path, include
from .views import OfferViews

urlpatterns = [
    path('', OfferViews.list_filter_offer, name='offer_list')
]
