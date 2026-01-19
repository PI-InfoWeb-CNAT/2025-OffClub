from django.urls import path, include
from .views import *

app_name = "enterprise"

urlpatterns = [
    path("register/", RegisterWizardView.as_view(FORMS), name="enterprise_register"),
    path("register/success/", RegisterDoneView.as_view(), name="registration_done"),
    path('dashboard/', EnterpriseDashboardView.as_view(), name='enterprise_dashboard'),
    path("dashboard/my_offers/<str:offer_id>/reviews/", SeeOfferReviewsView.as_view(), name="see_reviews"),
]

