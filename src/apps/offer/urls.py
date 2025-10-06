from django.urls import path
from .views import (
    OfferListView, OfferDetailJsonView,
    ManageOfferListView, ManageOfferDetailJsonView, ManageOfferCreateView, ManageOfferDeleteView, ManageOfferUpdateView
)

app_name = "offer"

urlpatterns = [
    path("", OfferListView.as_view(), name="list"),
    path("json/<uuid:offer_id>/", OfferDetailJsonView.as_view(), name="detail_json"),
    path("manage/", ManageOfferListView.as_view(), name="manage_list"),
    path("manage/json/<uuid:offer_id>/", ManageOfferDetailJsonView.as_view(), name="manage_detail_json"),
    path("manage/create/", ManageOfferCreateView.as_view(), name="manage_create"),
    path("manage/<uuid:pk>/edit/", ManageOfferUpdateView.as_view(), name="manage_edit"),
    path("manage/<uuid:pk>/delete/", ManageOfferDeleteView.as_view(), name="manage_delete"),
]
