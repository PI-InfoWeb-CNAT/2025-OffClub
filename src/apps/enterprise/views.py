from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from ..coupon.models import Coupon
from .services.see_evaluations import SeeEvaluationsService

class SeeCouponEvaluationsView(DetailView):
    model = Coupon
    template_name = "enterprise-dashboard/see_evaluations.html"
    context_object_name = "coupon"

    # Pega o id do cupom pela URL
    def get_object(self):
        return get_object_or_404(Coupon, id=self.kwargs.get("coupon_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coupon = self.object

        evaluations = SeeEvaluationsService.get_evaluations(coupon)
        stats = SeeEvaluationsService.evaluation_stats(coupon)
        final_price = SeeEvaluationsService.final_price(coupon.price, coupon.discount)

        context["evaluations"] = evaluations
        context["stats"] = stats
        context["final_price"] = final_price

        return context