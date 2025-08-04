from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from .services.offers_service import OfferService
from .models import Offer


class OfferListView(View):
    """
    Renderiza a página principal com a lista de ofertas e aplica filtros via GET.
    """
    def get(self, request, *args, **kwargs):
        name = request.GET.get('name', '')
        min_discount = request.GET.get('min_discount', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        page_num = request.GET.get('page')
        categories = request.GET.getlist('categories')

        context = OfferService.list_filter_offer(
            name, min_discount, start_date, end_date, page_num, categories
        )
        
        return render(request, 'offer.html', context)


class OfferDetailJsonView(View): 
    """
    Funciona como uma API: retorna os dados de uma oferta específica em JSON.
    """
    def get(self, request, *args, **kwargs):
        offer_id = kwargs.get('offer_id')
        offer = get_object_or_404(Offer, pk=offer_id)
        
        return JsonResponse(offer.to_dict())