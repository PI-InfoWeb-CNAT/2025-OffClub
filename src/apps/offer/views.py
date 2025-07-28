from django.shortcuts import render, redirect
from django.views import View
from ..offer.services.services import OfferService
from django.core.paginator import Paginator
from ..offer.models import *

class OfferViews(View):
    @staticmethod
    def list_filter_offer(request, *args, **kwargs):
        if request.method == 'GET':
            name = request.GET.get('name', '')
            filter_min_discount = request.GET.get('min_discount', '')
            filter_start_date = request.GET.get('start_date', '')
            filter_end_date = request.GET.get('end_date', '')   

        offers = OfferService.list_filter_offer(name, filter_min_discount, filter_start_date, filter_end_date)
        cheapOffers = OfferService.cheap_offers()
        offersCount = offers.__len__()

        offersPaginator = Paginator(offers, 8)
        pageNum = request.GET.get('page')
        if pageNum  == None:
            pageNum = 1
        
        page = offersPaginator.get_page(pageNum)
        startNum = (int(pageNum) - 1)*8 + 1
        endNum = int(pageNum) * 8

        pages = []
        p = 1
        while p <= offersPaginator.num_pages:
            pages.append(str(p))
            p = p + 1

        context = {'page' : page, 'pageNum': str(pageNum), 'endNum': endNum, 'startNum': startNum, 'offersCount': offersCount, 'cheapOffers' : cheapOffers, 'pages': pages}

        return render(request, 'offer.html', context)    