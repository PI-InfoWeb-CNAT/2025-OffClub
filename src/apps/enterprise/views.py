from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from ..coupon.models import Coupon
from .services.see_evaluations import SeeEvaluationsService

class SeeCouponEvaluationsView(LoginRequiredMixin, DetailView):
    model = Coupon
    template_name = "see_evaluations.html"
    context_object_name = "coupon"

    # Pega o id do cupom pela URL
    def get_object(self):
        return get_object_or_404(Coupon, id=self.kwargs.get("coupon_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coupon = self.get_object()

        evaluations = SeeEvaluationsService.get_evaluations(coupon)
        stars = SeeEvaluationsService.evaluation_stats(coupon)

        context["evaluations"] = evaluations
        context["stars"] = stars

        return context