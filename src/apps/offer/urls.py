from django.urls import path, include
from .views import OfferListView, OfferDetailView

urlpatterns = [
    path('', OfferListView.as_view(), name='offer_list'),
    path('detail/<uuid:offer_id>', OfferDetailView.as_view(), name='offer_detail'),
]
