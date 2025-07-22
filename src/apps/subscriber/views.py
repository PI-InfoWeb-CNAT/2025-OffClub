from urllib import request
from django.shortcuts import render
from apps.coupon.models import Coupon
from django.contrib.auth.decorators import login_required

def calculate_discount(price, discount_percentage):
    final_price = price - (price * discount_percentage /100)
    return price, final_price

@login_required
def historico(request):
    # logged_user = request.user
    # user_id = logged_user.id
    # user_coupons = Coupon.objects.filter(subscriber=user_id)
    #context = {'coupons': user_coupons}
    objects = Coupon.objects.all()
    coupons = []
    for coupon in objects:
        price = coupon.offer.price
        discount = coupon.offer.discount
        old_price, final_price = calculate_discount(price, discount)
        coupon_data = {
                'old_price':     old_price,
                'final_price':   final_price,
            }
        dic = {'object': coupon, 'data': coupon_data}
        coupons.append(dic)
    context = {'coupons': coupons}
    return render(request, 'subscriber.html', context=context, status=200)