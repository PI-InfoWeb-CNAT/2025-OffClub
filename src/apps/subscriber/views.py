from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView
from formtools.wizard.views import SessionWizardView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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

    template_name = "subscriber_coupons.html"

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
        
        req_month = self.request.GET.get('month')
        req_year = self.request.GET.get('year')
        req_order = self.request.GET.get('order', 'recent')
        ordering = "creation_date" if req_order == 'old' else "-creation_date"

        coupons = (
            Coupon.objects.filter(subscriber=subscriber)
            .select_related("offer", "offer__enterprise", "offer__enterprise__user")
            .order_by(ordering)
        )

        active_coupons = []
        used_coupons = []
        years = set()

        for coupon in coupons:
            # --- LÓGICA DE POPULAR O FILTRO DE ANOS ---
            # Adicionamos ao set ANTES de filtrar, para que o dropdown mostre todos os anos disponíveis
            # independentemente do filtro atual.
            if coupon.used_date:
                years.add(coupon.used_date.year)

            # --- LÓGICA DE FILTRAGEM (PYTHON) ---
            # Se tiver filtro de Mês ou Ano, verificamos se o cupom atende.
            # Se não atender, usamos 'continue' para pular este item do loop.
            
            is_filtered = False
            
            # Se estamos filtrando por data, Cupons Ativos (sem data de uso) geralmente são ocultados
            # ou você pode decidir mostrá-los sempre. Aqui assumo que filtro de data = histórico.
            has_date_filter = (req_month and req_month != 'all') or (req_year and req_year != 'all')

            if coupon.used_date:
                # Validação do Mês
                if req_month and req_month != 'all' and coupon.used_date.month != int(req_month):
                    is_filtered = True
                
                # Validação do Ano
                if req_year and req_year != 'all' and coupon.used_date.year != int(req_year):
                    is_filtered = True
            else:
                # Cupom Ativo: Se o usuário filtrou por uma data específica (ex: Janeiro/2023),
                # ocultamos os ativos pois eles não pertencem a essa data passada.
                if has_date_filter:
                    is_filtered = True

            if is_filtered:
                continue # Pula para o próximo cupom, não adiciona na lista visual

            # --- FIM DA FILTRAGEM, SEGUE SEU CÓDIGO ORIGINAL ---

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
                # Nota: years.add movido para o topo do loop
            else:
                active_coupons.append(coupon_payload)

        items_per_page = 2  # Quantos itens por seção
        
        paginator_active = Paginator(active_coupons, items_per_page)
        paginator_used = Paginator(used_coupons, items_per_page)

        page_number = self.request.GET.get('page', 1)

        # 1. Pega a página dos ATIVOS (ou lista vazia se não existir)
        try:
            active_page_obj = paginator_active.page(page_number)
        except (EmptyPage, PageNotAnInteger):
            active_page_obj = [] 

        # 2. Pega a página dos USADOS (ou lista vazia se não existir)
        try:
            used_page_obj = paginator_used.page(page_number)
        except (EmptyPage, PageNotAnInteger):
            used_page_obj = []

        # 3. Dados manuais para a barra de paginação (ISTO SUBSTITUI O master_page_obj)
        max_pages = max(paginator_active.num_pages, paginator_used.num_pages)
        
        try:
            current_page = int(page_number)
        except ValueError:
            current_page = 1

        context.update(
            {
                "active_coupons": active_page_obj,
                "used_coupons": used_page_obj,
                
                # Dados manuais que o template vai usar
                "current_page": current_page,
                "max_pages": max_pages,
                "page_range": range(1, max_pages + 1), 
                "has_next": current_page < max_pages,
                "has_previous": current_page > 1,
                "next_page": current_page + 1,
                "previous_page": current_page - 1,
                "years_group": sorted(years, reverse=True),
                "form": EvaluationForm(),
                "selected_month": int(req_month) if req_month and req_month != 'all' else 'all',
                "selected_year": int(req_year) if req_year and req_year != 'all' else 'all',
                "selected_order": req_order,
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
        subscriber = getattr(request.user, "subscriber", None)
        address = request.user.addresses.first() if request.user.is_authenticated else None
        phone = request.user.phones.first() if request.user.is_authenticated else None

        active_subscription = getattr(subscriber, "active_subscription", None) if subscriber else None

        if (not active_subscription or not active_subscription.plan) and request.user.is_authenticated:
            # Busca a assinatura ativa mais recente vinculada ao usuário.
            user_subscriptions = request.user.subscriptions.select_related("plan").order_by("-start_date")
            for subscription in user_subscriptions:
                if subscription.plan and subscription.is_active:
                    active_subscription = subscription
                    break

        plan_info = None
        if active_subscription and active_subscription.plan and active_subscription.is_active:
            plan = active_subscription.plan
            duration_display = "-"
            duration = plan.duration
            if duration:
                total_days = duration.days
                total_seconds = duration.seconds
                if total_days > 0 and total_seconds == 0:
                    duration_display = f"{total_days} dia{'s' if total_days != 1 else ''}"
                else:
                    duration_display = str(duration)

            plan_info = {
                "title": plan.title,
                "price": plan.price,
                "duration": duration_display,
            }

        context = {
            "subscriber": subscriber,
            "user": request.user,
            "address": address,
            "phone": phone,
            "subscription": active_subscription,
            "plan_info": plan_info,
        }
        return render(request, "profile/personal_data.html", context)
    