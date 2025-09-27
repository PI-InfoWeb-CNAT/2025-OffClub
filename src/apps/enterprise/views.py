from urllib import request
from django.shortcuts import render, redirect
from apps.coupon.models import Coupon
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views import View
# Create your views here.

class EnterpriseViews(View):
    @staticmethod
    def enterprise_register(request):
        if request.method == 'GET':
            context = {
                "hello": "world"
            }
            return render(request, "enterprise.html", context=context)
