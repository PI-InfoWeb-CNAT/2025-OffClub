from django.urls import path
from .views import (
    OfferListView,
    OfferDetailJsonView,
    OfferFilterAjaxView,
    ManageOfferListView,
    ManageOfferDetailView,
    ManageOfferDetailJsonView,
    ManageOfferCreateView,
    ManageOfferDeleteView,
    ManageOfferUpdateView,
)
from django.views.generic import RedirectView

app_name = "offer"

urlpatterns = [
    path("", OfferListView.as_view(), name="list"),
    path("json/<uuid:offer_id>/", OfferDetailJsonView.as_view(), name="detail_json"),
    path("filter/", OfferFilterAjaxView.as_view(), name="filter_ajax"),
    path("manage/", ManageOfferListView.as_view(), name="manage_list"),
    path(
        "manage/<uuid:offer_id>/", ManageOfferDetailView.as_view(), name="manage_detail"
    ),
    path(
        "json/<uuid:offer_id>/",
        ManageOfferDetailJsonView.as_view(),
        name="manage_detail_json",
    ),
    path("manage/create/", ManageOfferCreateView.as_view(), name="manage_create"),
    path("manage/<uuid:pk>/edit/",
         ManageOfferUpdateView.as_view(), name="manage_edit"),
    path(
        "manage/<uuid:pk>/delete/",
        ManageOfferDeleteView.as_view(),
        name="manage_delete",
    ),
    path(
        "list/",
        RedirectView.as_view(
            pattern_name="offer:manage_list", permanent=False),
        name="offer_list",
    ),
]
