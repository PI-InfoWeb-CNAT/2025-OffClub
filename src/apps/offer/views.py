from django.shortcuts import render, redirect
from ..offer.models import *

# Create your views here.


# Create your views here.
class OfferViews:
    @staticmethod
    def list_filter_offer(request):
        return render(request, template_name='offer.html', status=200)