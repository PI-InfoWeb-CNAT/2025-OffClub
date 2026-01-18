from django.http import JsonResponse
import uuid
from django.db import transaction, IntegrityError
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy # O reverse_lazy() serve para atributos de classe ou variáveis 
                                     # globais que o Django ainda não terminou de carregar no projeto
from django.utils import timezone
from .models import Offer
from .forms.offer_form import OfferForm
from .services.manage_offer import ManageOffer
from .services.offers_service import OfferService
from apps.coupon.models import Coupon
from apps.subscriber.models import Subscriber

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

class RedeemCouponView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        offer_id = kwargs.get("offer_id")
        subscriber = get_object_or_404(Subscriber, user=request.user)

        try:
            with transaction.atomic():
                offer = Offer.objects.select_for_update().get(pk=offer_id)

                now = timezone.now()
                if not (offer.start_date <= now <= offer.end_date):
                    return JsonResponse(
                        {"ok": False, "error": "Oferta indisponível no momento."},
                        status=400,
                    )

                if offer.generated_coupons >= offer.max_coupons:
                    return JsonResponse(
                        {"ok": False, "error": "Oferta esgotada."},
                        status=400,
                    )

                expiration_date = timezone.now() + offer.redemption_period

                coupon, created = Coupon.objects.get_or_create(
                    subscriber=subscriber,
                    offer=offer,
                    defaults={
                        "code": uuid.uuid4().hex[:10].upper(),
                        "expiration_date": expiration_date,
                    },
                )

                if created:
                    Offer.objects.filter(pk=offer.pk).update(
                        generated_coupons=F("generated_coupons") + 1
                    )

                offer.refresh_from_db(fields=["generated_coupons", "max_coupons"])
                remaining = offer.max_coupons - offer.generated_coupons

                return JsonResponse(
                    {
                        "ok": True,
                        "created": created,
                        "coupon_id": str(coupon.id),
                        "remaining_coupons": remaining,
                        "max_coupons": offer.max_coupons,
                    },
                    status=200,
                )

        except Offer.DoesNotExist:
            return JsonResponse({"ok": False, "error": "Oferta não encontrada."}, status=404)

        except IntegrityError as e:
            print("INTEGRITY ERROR:", repr(e))
            return JsonResponse(
                {"ok": False, "error": "Falha ao criar cupom. Tente novamente."},
                status=409,
            )
    

class ManageOfferListView(TemplateView):
    template_name = "offer_list.html" 

    def get_context_data(self, **kwargs):
        from django.utils import timezone
from django.views.generic import TemplateView
from .services.manage_offer import ManageOffer

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
