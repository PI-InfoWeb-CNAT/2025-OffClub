from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy # O reverse_lazy() serve para atributos de classe ou variáveis 
                                     # globais que o Django ainda não terminou de carregar no projeto
from django.utils import timezone
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from .models import Offer
from .forms.offer_form import OfferForm
from .services.manage_offer import ManageOffer
from .services.offers_service import OfferService

class OfferListView(View):
    
    def get(self, request, *args, **kwargs):
        name = request.GET.get('name', '')
        min_discount = request.GET.get('min_discount', '')
        page_num = request.GET.get('page')
        categories = request.GET.getlist('categories')

        context = OfferService.list_filter_offer(
            name, min_discount, page_num, categories
        )
        
        return render(request, 'offer.html', context)


class OfferFilterAjaxView(View):
    """View para filtrar ofertas via AJAX sem recarregar a página"""
    
    def get(self, request, *args, **kwargs):
        name = request.GET.get('name', '')
        min_discount = request.GET.get('min_discount', '')
        page_num = request.GET.get('page', 1)
        categories = request.GET.getlist('categories')

        context = OfferService.list_filter_offer(
            name, min_discount, page_num, categories
        )
        
        # Renderiza apenas o HTML das ofertas
        offers_html = render_to_string('components/offers_results.html', context, request=request)
        
        return JsonResponse({
            'html': offers_html,
            'count': context['offersCount'],
            'has_next': context['page_obj'].has_next(),
            'has_previous': context['page_obj'].has_previous(),
            'current_page': context['page_obj'].number,
            'total_pages': context['page_obj'].paginator.num_pages,
        })


class OfferDetailJsonView(View): 
    def get(self, request, *args, **kwargs):
        offer_id = kwargs.get('offer_id')
        offer = get_object_or_404(Offer, pk=offer_id)
        data = offer.to_dict()

        # Indica ao front-end se o usuário já resgatou essa oferta
        subscriber = getattr(request.user, 'subscriber', None)
        if subscriber:
            from apps.coupon.models import Coupon
            data['already_redeemed'] = Coupon.objects.filter(subscriber=subscriber, offer=offer).exists()
        else:
            data['already_redeemed'] = False

        return JsonResponse(data)
    

class RedeemOfferView(LoginRequiredMixin, View):
    """API para resgatar um cupom de uma oferta via requisição AJAX."""

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        from apps.coupon.models import Coupon

        subscriber = getattr(request.user, "subscriber", None)
        if subscriber is None:
            return JsonResponse({"error": "Usuário precisa ser um assinante."}, status=403)

        offer_id = kwargs.get("offer_id")
        offer = get_object_or_404(Offer, pk=offer_id)

        if not offer.is_active:
            return JsonResponse({"error": "Oferta indisponível."}, status=400)

        # Protege contra condições de corrida usando bloqueio transacional
        with transaction.atomic():
            offer_locked = Offer.objects.select_for_update().get(pk=offer.pk)
            remaining = offer_locked.max_coupons - offer_locked.generated_coupons

            if remaining <= 0:
                return JsonResponse({"error": "Oferta esgotada."}, status=400)

            if Coupon.objects.filter(subscriber=subscriber, offer=offer_locked).exists():
                return JsonResponse({"error": "Você já resgatou essa oferta."}, status=400)

            coupon = Coupon.objects.create(subscriber=subscriber, offer=offer_locked)
            offer_locked.generated_coupons += 1
            offer_locked.save(update_fields=["generated_coupons"])

        return JsonResponse({
            "success": True,
            "coupon": {
                "id": str(coupon.id),
                "code": coupon.code,
                "expiration_date": coupon.expiration_date.isoformat(),
            },
            "remaining_coupons": offer_locked.max_coupons - offer_locked.generated_coupons,
        }, status=201)

class ManageOfferListView(TemplateView):
    template_name = "offer_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            ManageOffer.list_filter_offer(
                name=self.request.GET.get("q"),
                filter_min_discount=self.request.GET.get("min_discount"),
                filter_start_date=self.request.GET.get("start"),
                filter_end_date=self.request.GET.get("end"),
                pageNum=self.request.GET.get("page"),
                filter_categories=self.request.GET.getlist("category"),
                per_page=8,
                only_active=True,
            )
        )
        ctx["now"] = timezone.now()
        return ctx


class ManageOfferDetailView(View):
    def get(self, request, *args, **kwargs):
        offer_id = kwargs.get('offer_id') or kwargs.get('pk')
        try:
            offer = ManageOffer.get(pk=offer_id)
        except Offer.DoesNotExist:
            offer = get_object_or_404(Offer, pk=offer_id)
        remaining = (
            getattr(offer, 'remaining_coupons', None)  # Acessa um atributo de um objeto pelo nome, como se o nome fosse uma string 
            or (offer.to_dict().get('remaining_coupons') if hasattr(offer, 'to_dict') else None)  # verifica se tem atributo antes de acessar
            or 0  # fallback
        )
        context = {
            'offer': offer,
            'remaining_coupons': remaining,
        }
        return render(request, 'offer_detail_enterprise.html', context)


class ManageOfferDetailJsonView(View):
    def get(self, request, *args, **kwargs):
        offer_id = kwargs.get('offer_id') or kwargs.get('pk')
        offer = get_object_or_404(Offer, pk=offer_id)
        return JsonResponse(offer.to_dict(), safe=False, json_dumps_params={'ensure_ascii': False})
    
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
    template_name = "offer_confirm_delete.html"
    success_url = reverse_lazy("offer:manage_list")
