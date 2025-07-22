from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from ..offer.models import *

class OfferViews(View):
    @staticmethod
    def list_filter_offer(self, request, *args, **kwargs):
        return render(request, template_name='offer.html', status=200)
    @staticmethod
    def offer(self, request, *args, **kwargs):
        if request.method == 'GET':
            offers = Offer.objects.filter(end_date < timezone.now())
            context = {'offers': offers}
            return render(request, 'offer_detail.html', context)

