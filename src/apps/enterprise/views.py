import logging

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView
from django.core.files.storage import FileSystemStorage

from apps.enterprise.services.see_evaluations import SeeEvaluationsService
from .forms import (
    EnterpriseInfoForm,
    CredentialsForm,
    ContactForm,
    ProfilePicForm,
    LoginForm
)
from formtools.wizard.views import SessionWizardView
from apps.users.models import User
from .models import Enterprise, LineOfBusiness
from apps.coupon.models import Coupon
from apps.core.models import Address, Phone


logger = logging.getLogger(__name__)


FORMS = [
    ("info", EnterpriseInfoForm),
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

class RegisterWizardView(SessionWizardView):
    # Serve pro wizard salvar os arquivos temporariamente
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
            is_active=False,
            user_role=User.UserRole.ENTERPRISE,
        )
        if data.get("password"):
            user.set_password(data["password"])
        user.save()

        enterprise = Enterprise.objects.create(
            user=user,
            corporate_reason=data.get("corporate_reason", ""),
            trade_name=data.get("trade_name", ""),
            description=data.get("description", ""),
            cnpj=data.get("cnpj", ""),
            line_of_business=data.get("line_of_business")
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
        
        if data.get("phone_number2"):
            Phone.objects.create(
                phone_number=data.get("phone_number2"),
                phone_type=Phone.PhoneType.OTHER,
                user=user,
            )

        enterprise.save()
        return redirect("enterprise:registration_done")

class RegisterDoneView(TemplateView):
    template_name = 'register/done.html'
    

class SeeCouponEvaluationsView(DetailView):
    model = Coupon
    template_name = "enterprise-dashboard/see_avaluations.html"
    context_object_name = "coupon"

    # Pega o id do cupom pela URL
    def get_object(self):
        return get_object_or_404(Coupon, id=self.kwargs.get("coupon_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coupon = self.get_object()

        evaluations = SeeEvaluationsService.get_evaluations(coupon)
        stats = SeeEvaluationsService.evaluation_stats(coupon)
        final_price = SeeEvaluationsService.final_price(coupon.offer.price, coupon.offer.discount)

        context["evaluations"] = evaluations
        context["stats"] = stats
        context["final_price"] = final_price

        return context


class EnterpriseDashboardView(View):
    template_name = 'enterprise-dashboard/enterprise_dashboard.html'
    
    def get(self, request):
        return render(request, 'enterprise-dashboard/enterprise_dashboard.html')
