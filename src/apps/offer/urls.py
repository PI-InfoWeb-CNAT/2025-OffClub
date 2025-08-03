from django.urls import path, include
from .views import OfferListView, OfferDetailJsonView

urlpatterns = [
    path('', OfferListView.as_view(), name='offer_list'),
    path('json/<uuid:offer_id>/', OfferDetailJsonView.as_view(), name='offer_detail_json'),
]
