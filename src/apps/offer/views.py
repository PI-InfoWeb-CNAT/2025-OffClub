from django.shortcuts import render, redirect
from django.views import View
from .services.offers_service import OfferService
from ..offer.models import *

class OfferViews(View):
    @staticmethod
    def offer(request, *args, **kwargs):
        name = request.GET.get('name', '')
        filter_min_discount = request.GET.get('min_discount', '')
        filter_start_date = request.GET.get('start_date', '')
        filter_end_date = request.GET.get('end_date', '')
        pageNum = request.GET.get('page')
        filter_categories = request.GET.getlist('categories')

        context = OfferService.list_filter_offer(name, filter_min_discount, filter_start_date, filter_end_date, pageNum, filter_categories)
        return render(request, 'offer.html', context)   


class OfferDetailViews(View):
    template_name = 'offer_detail.html'
    @staticmethod
    def offer(request, *args, **kwargs):
        """
        Este método agora funciona corretamente mantendo a estrutura original.
        """
        if request.method == 'GET':
            offers = Offer.objects.filter(end_date__gte=timezone.now())
            context = {'filterOffers': offers}
            return render(request, 'offer_detail.html', context)

        if request.method == 'POST':
            queryset = Offer.objects.filter(end_date__gte=timezone.now())
            
            filter_min_discount = request.POST.get('min_discount')
            filter_start_date = request.POST.get('start_date')
            filter_end_date = request.POST.get('end_date')

            if filter_min_discount:
                try:
                    min_discount_value = float(filter_min_discount)
                    queryset = queryset.filter(discount__gt=min_discount_value)
                except (ValueError, TypeError):
                    pass
        
            if filter_start_date:
                queryset = queryset.filter(start_date__gte=filter_start_date)

            if filter_end_date:
                queryset = queryset.filter(end_date__lte=filter_end_date)

            context = {
                'filterOffers': queryset,
                'form_data': request.POST 
            }
            
            return render(request, 'offer_detail.html', context)
        return render(request, 'offer.html', context)    
