from django.urls import path, include
from .views import SeeCouponEvaluationsView

app_name = "enterprise"

urlpatterns = [
    path("dashboard/my_offers/<str:coupon_id>/evaluations/", SeeCouponEvaluationsView.as_view(), name="see_evaluations"),
]