from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from ..coupon.models import Coupon
from .services.see_evaluations import SeeEvaluationsService
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from apps.users.forms import EnterpriseSignUpForm

class EnterpriseSignUpView(CreateView):
    """
    Renderiza e processa o formulário de registro para novas empresas.
    """
    form_class = EnterpriseSignUpForm
    template_name = 'registration/signup_form.html'
    
    sucess_url = reverse_lazy('enterprise_signup_done')
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'enterprise'
        return super().get_context_data(**kwargs)
    
def enterprise_signup_done(request):
    """
    Página de sucesso exibida após o registro bem sucedido.
    """
    return render(request, 'registration/signup_done.html')

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
