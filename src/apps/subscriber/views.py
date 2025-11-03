from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView
from formtools.wizard.views import SessionWizardView

from apps.core.models import Address, Phone
from apps.coupon.models import Coupon
from apps.users.models import User

from .forms import (
    ContactForm,
    CredentialsForm,
    EvaluationForm,
    LoginForm,
    PersonalInfoForm,
    ProfilePicForm,
)
from .models import Evaluation, Subscriber
from .services.discount import DiscountService
from .services.evaluation import EvaluationService


FORMS = [
    ("info", PersonalInfoForm),
    ("login", CredentialsForm),
    ("contact", ContactForm),
    ("pfp", ProfilePicForm),
]

TEMPLATES = {
    "info": "register/step_1.html",
    "login": "register/step_2.html",
    "contact": "register/step_3.html",
    "pfp": "register/step_4.html",
}


class LoginView(View):
    """Tela de login do assinante."""

    def get(self, request):
        form = LoginForm()
        next_url = request.GET.get("next") or "/"
        return render(
            request,
            "login.html",
            {
                "form": form,
                "next": next_url,
            },
        )

    def post(self, request):
        form = LoginForm(request.POST)
        next_url = request.POST.get("next") or "/"

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(next_url)
            form.add_error(None, "Credenciais inválidas")

        return render(
            request,
            "login.html",
            {
                "form": form,
                "next": next_url,
            },
        )


class RegisterWizardView(SessionWizardView):
    """Wizard multi-etapas para registro de assinantes."""

    file_storage = FileSystemStorage()
    form_list = FORMS

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        data = {}
        for form in form_list:
            if hasattr(form, "cleaned_data"):
                data.update(form.cleaned_data)

        user = User.objects.create(
            email=data.get("email"),
            profile_picture=data.get("profile_picture"),
            is_active=True,
            user_role=User.UserRole.SUBSCRIBER,
        )
        if data.get("password"):
            user.set_password(data["password"])
        user.save()

        subscriber = Subscriber.objects.create(
            user=user,
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            cpf=data.get("cpf", ""),
            birth_date=data.get("birth_date"),
        )

        if data.get("cep") or data.get("street_name"):
            Address.objects.create(
                user=user,
                cep=data.get("cep", ""),
                city=data.get("city", ""),
                state=data.get("state", ""),
                neighborhood=data.get("neighborhood", ""),
                street_name=data.get("street_name", ""),
                number=data.get("number", ""),
                complement=data.get("complement", ""),
            )

        if data.get("phone_number"):
            Phone.objects.create(
                phone_number=data.get("phone_number"),
                phone_type=Phone.PhoneType.MOBILE,
                user=user,
            )

        subscriber.save()
        return redirect("subscriber:registration_done")


class HistoryView(LoginRequiredMixin, TemplateView):
    """Dashboard do assinante com histórico de cupons."""

    template_name = "subscriber.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subscriber = getattr(self.request.user, "subscriber", None)

        if subscriber is None:
            context.update(
                {
                    "active_coupons": [],
                    "used_coupons": [],
                    "years_group": [],
                    "form": EvaluationForm(),
                }
            )
            return context

        coupons = (
            Coupon.objects.filter(subscriber=subscriber)
            .select_related("offer", "offer__enterprise", "offer__enterprise__user")
            .order_by("-creation_date")
        )

        active_coupons = []
        used_coupons = []
        years = set()

        for coupon in coupons:
            old_price, final_price = DiscountService.final_price(
                coupon.offer.price,
                coupon.offer.discount,
            )

            coupon_payload = {
                "object": coupon,
                "data": {
                    "old_price": old_price,
                    "final_price": final_price,
                    "used_month": coupon.used_date.month if coupon.used_date else None,
                },
            }

            if coupon.used_date:
                used_coupons.append(coupon_payload)
                years.add(coupon.used_date.year)
            else:
                active_coupons.append(coupon_payload)

        context.update(
            {
                "active_coupons": active_coupons,
                "used_coupons": used_coupons,
                "years_group": sorted(years, reverse=True),
                "form": EvaluationForm(),
            }
        )
        return context


class RegistrationDone(TemplateView):
    """Tela exibida após o cadastro concluído."""

    template_name = "register/done.html"


class EvaluationCreateView(LoginRequiredMixin, View):
    """Recebe avaliações de cupons via requisições AJAX."""

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        form = EvaluationForm(request.POST)
        if not form.is_valid():
            errors = {
                field: [str(error) for error in error_list]
                for field, error_list in form.errors.items()
            }
            return JsonResponse({"success": False, "errors": errors}, status=400)

        coupon = get_object_or_404(Coupon, id=kwargs.get("coupon_id"))
        subscriber = getattr(request.user, "subscriber", None)

        if subscriber is None or coupon.subscriber != subscriber:
            return JsonResponse(
                {"error": "Esse cupom não pertence ao usuário logado."},
                status=403,
            )

        if Evaluation.objects.filter(coupon=coupon).exists():
            return JsonResponse(
                {"error": "Você já avaliou este cupom."},
                status=400,
            )

        EvaluationService.create_evaluation(
            coupon=coupon,
            stars=form.cleaned_data.get("stars"),
            message=form.cleaned_data.get("message", ""),
        )

        return JsonResponse(
            {"success": "Avaliação registrada com sucesso!"},
            status=200,
        )





# PERFIL DE USUÁRIO

class ProfileView(View):
    def get(self, request):
        return render(request, "profile/personal_data.html")
    