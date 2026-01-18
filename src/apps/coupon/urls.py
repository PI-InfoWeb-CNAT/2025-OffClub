from django.urls import path, include
from .views import CouponDetailView
app_name = "coupon"

urlpatterns = [
    path('detail/<uuid:coupon_id>/', CouponDetailView.as_view(), name='coupon_detail')
]


