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
        coupon_id = self.kwargs.get("coupon_id")
        coupon = Coupon.objects.get(id=coupon_id)
        stars = form.cleaned_data.get("stars")
        message = form.cleaned_data.get("message", "")

        if Evaluation.objects.filter(coupon=coupon).exists():
            return JsonResponse({"error": "Você já avaliou este cupom."}, status=400)

        EvaluationService.create_evaluation(coupon, stars, message)

        return JsonResponse({"success": "Avaliação registrada com sucesso!"}, status=200)

    def form_invalid(self, form):
        errors = {field: [str(err) for err in errs] for field, errs in form.errors.items()}
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": errors})
        return super().form_invalid(form)