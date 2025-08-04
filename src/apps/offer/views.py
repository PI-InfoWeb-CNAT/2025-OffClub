from django.shortcuts import render, redirect
from ..offer.models import *

def offer(request):
    return render(request, 'offer_detail.html')

class OfferViews:
    @staticmethod
    def list_filter_offer(request):
        return render(request, template_name='offer.html', status=200)

