from urllib import request
from django.shortcuts import render, redirect
from apps.coupon.models import Coupon
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views import View
from apps.subscriber.services.services import ServiceDiscount

class SubscriberViews(View):
    @staticmethod
    # @login_required
    def historico(request):
        if request.method == 'GET':
            # logged_user = request.user
            # user_id = logged_user.id
            # user_coupons = Coupon.objects.filter(subscriber=user_id)
            #context = {'coupons': user_coupons}
            used_filtered = Coupon.objects.filter(used_date__isnull=False).order_by('-used_date')
            active_filtered = Coupon.objects.filter(used_date__isnull=True)
            used_coupons = []
            active_coupons = []
            for coupon in used_filtered:
                price = coupon.offer.price
                discount = coupon.offer.discount
                old_price, final_price = ServiceDiscount.final_price(price, discount)
                coupon_data = {
                        'old_price':     old_price,
                        'final_price':   final_price,
                        'used_month':    coupon.used_date.month,
                    }
                dic = {'object': coupon, 'data': coupon_data}
                used_coupons.append(dic)

            for coupon in active_filtered:
                price = coupon.offer.price
                discount = coupon.offer.discount
                old_price, final_price = ServiceDiscount.final_price(price, discount)
                coupon_data = {
                        'old_price':     old_price,
                        'final_price':   final_price,
                        'used_month': None,
                    }
                dic = {'object': coupon, 'data': coupon_data}
                active_coupons.append(dic)
            context = {'used_coupons': used_coupons, 'active_coupons': active_coupons}
            return render(request, 'subscriber.html', context=context, status=200)