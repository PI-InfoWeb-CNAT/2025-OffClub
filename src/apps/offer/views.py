from django.shortcuts import render, redirect
from django.views import View
from ..offer.services.services import OfferService
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