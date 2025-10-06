from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from .services.offers_service import OfferService
from .models import Offer
from django.urls import reverse_lazy #O reverse_lazy() serve para atributos de classe ou variáveis globais que o Django ainda não terminou de carregar no projeto
from django.utils import timezone
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.utils import timezone
from .services.manage_offer import ManageOffer
from .models import Offer, OfferForm 


class OfferListView(View):
    
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
    def get(self, request, *args, **kwargs):
        offer_id = kwargs.get('offer_id')
        offer = get_object_or_404(Offer, pk=offer_id)
        
        return JsonResponse(offer.to_dict())
    

class ManageOfferListView(TemplateView):
    template_name = "offer_list.html" 

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            ManageOffer.list_filter_offer(
                name=self.request.GET.get("q") or "",
                filter_min_discount=self.request.GET.get("min_discount") or "",
                filter_start_date=self.request.GET.get("start") or "",
                filter_end_date=self.request.GET.get("end") or "",
                pageNum=self.request.GET.get("page"),
                filter_categories=self.request.GET.getlist("category") or None,
                per_page=8,
                only_active=True,
            )
        )
        ctx["now"] = timezone.now()  
        return ctx


class ManageOfferDetailJsonView(View):
    def get(self, request, *args, **kwargs):
        offer = get_object_or_404(Offer, pk=kwargs.get("offer_id"))
        return JsonResponse(offer.to_dict())

class ManageOfferCreateView(CreateView):
    model = Offer
    form_class = OfferForm
    template_name = "offer_form.html"
    success_url = reverse_lazy("offer:manage_list") 


class ManageOfferUpdateView(UpdateView):
    model = Offer
    form_class = OfferForm
    template_name = "offer_form.html"
    success_url = reverse_lazy("offer:manage_list")


class ManageOfferDeleteView(DeleteView):
    model = Offer
    template_name = "offer/offer_confirm_delete.html"
    success_url = reverse_lazy("offer:manage_list")
