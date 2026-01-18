from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from apps.coupon.models import Coupon
from datetime import datetime

class CouponDetailView(View):
    def get(self, request, *args, **kwargs):
        coupon_id = kwargs.get('coupon_id') or kwargs.get('pk')

        coupon = get_object_or_404(Coupon, pk=coupon_id)

        offer = coupon.offer

        context = {
            'coupon': coupon,
            'offer': offer,
        }
        return render(request, 'coupon.html', context)