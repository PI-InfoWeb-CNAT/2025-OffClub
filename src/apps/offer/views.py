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
            context = {'filterOffers': offers}
            return render(request, 'offer_detail.html', context)
        if request.method == 'POST':
            offers = Offer.objects.filter(end_date < timezone.now())
            filter_min_discount = request.POST.get('min_discount', '')
            filter_start_date = request.POST.get('start_date', '')
            filter_end_date = request.POST.get('end_date', '')
            if filter_min_discount:
                offers = offers.filter(discount > filter_min_discount)
            if filter_start_date:
                if filter_end_date:
                    offers = offers.filter(filter_start_date < end_date < filter_end_date)
                else:
                    offers = offers.filter(filter_start_date < end_date)
            elif filter_end_date:
                offers = offers.filter(end_date < filter_end_date)
            context = {'filterOffers': offers}
            return render(request, 'offer_detail.html', context)       