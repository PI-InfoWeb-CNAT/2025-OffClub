from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Coupon, Evaluation
from .forms.evaluation_form import EvaluationForm
from .services.services import EvaluationService
    

class EvaluationCreateView(LoginRequiredMixin, CreateView):
    """
    Salva no banco de dados o formulário com as respostas
    da avaliação do cupom preenchido pelo usuário
    """

    model = Evaluation
    form_class = EvaluationForm
    template_name = "components/evaluate_coupon.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        coupon_id = self.request.POST.get("coupon_id")
        self.coupon = get_object_or_404(Coupon, id=coupon_id)
        form.instance.coupon = self.coupon

        stars = form.cleaned_data.get("stars")
        message = form.cleaned_data.get("message", "")

        if Evaluation.objects.filter(coupon=self.coupon, user=self.request.user).exists():
            if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "errors": {"__all__": ["Este cupom já foi avaliado."]}})
            return redirect("subscriber:historico_consumo")

        EvaluationService.create_evaluation(self.coupon, stars, message)

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})

        messages.success(self.request, "Avaliação registrada com sucesso!")
        return redirect("subscriber:historico_consumo")

    def form_invalid(self, form):
        errors = {field: [str(err) for err in errs] for field, errs in form.errors.items()}
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": errors})
        return super().form_invalid(form)