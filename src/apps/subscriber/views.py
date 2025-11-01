from urllib import request
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Coupon, Evaluation
from .forms.evaluation_form import EvaluationForm
from .services.services import EvaluationService, ServiceDiscount

class SubscriberViews(View):
    @staticmethod
    # @login_required
    def consumption_history_list(request):
        if request.method == 'GET':
            # logged_user = request.user
            # user_id = logged_user.id
            # user_coupons = Coupon.objects.filter(subscriber=user_id)
            #context = {'coupons': user_coupons}
            used_filtered = Coupon.objects.filter(used_date__isnull=False).order_by('-used_date')
            active_filtered = Coupon.objects.filter(used_date__isnull=True)
            used_coupons = []
            active_coupons = []
            years_group = []
            for coupon in used_filtered:
                price = coupon.offer.price
                discount = coupon.offer.discount
                old_price, final_price = ServiceDiscount.final_price(price, discount)
                coupon_data = {
                        'old_price':     old_price,
                        'final_price':   final_price,
                        'used_month':    coupon.used_date.month,
                        'used_year': coupon.used_date.year,
                    }
                dic = {'object': coupon, 'data': coupon_data}
                if coupon_data['used_year'] not in years_group:
                    years_group.append(coupon_data['used_year'])
                used_coupons.append(dic)

            for coupon in active_filtered:
                price = coupon.offer.price
                discount = coupon.offer.discount
                old_price, final_price = ServiceDiscount.final_price(price, discount)
                coupon_data = {
                        'old_price':     old_price,
                        'final_price':   final_price,
                        'used_month': None,
                    }
                dic = {'object': coupon, 'data': coupon_data}
                active_coupons.append(dic)
            context = {'used_coupons': used_coupons, 'active_coupons': active_coupons, 'years_group': years_group, 'form': EvaluationForm(),}
            return render(request, 'subscriber.html', context=context, status=200)
            

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

        # usuário logado
        subscriber = self.request.user.subscriber

        # verifica se o assinante já fez uma avaliação
        if Evaluation.objects.filter(coupon=coupon, coupon__subscriber=subscriber).exists():
            return JsonResponse({"error": "Você já avaliou este cupom."}, status=400)

        # cria uma nova avaliação
        EvaluationService.create_evaluation(coupon, stars, message)

        return JsonResponse({"success": "Avaliação registrada com sucesso!"}, status=200)

    def form_invalid(self, form):
        errors = {field: [str(err) for err in errs] for field, errs in form.errors.items()}
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": errors})
        return super().form_invalid(form)