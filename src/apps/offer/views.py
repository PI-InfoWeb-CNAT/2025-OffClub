from django.shortcuts import render
from django.utils import timezone
from django.views import View
from ..offer.models import Offer

class OfferViews(View):
    @staticmethod
    def list_filter_offer(request, *args, **kwargs):
        return render(request, template_name='offer.html', status=200)

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