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
            objects = Coupon.objects.all()
            coupons = []
            for coupon in objects:
                price = coupon.offer.price
                discount = coupon.offer.discount
                old_price, final_price = ServiceDiscount.final_price(price, discount)
                coupon_data = {
                        'old_price':     old_price,
                        'final_price':   final_price,
                    }
                dic = {'object': coupon, 'data': coupon_data}
                coupons.append(dic)
            context = {'coupons': coupons}
            return render(request, 'subscriber.html', context=context, status=200)