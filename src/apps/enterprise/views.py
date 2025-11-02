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


FORMS = [
    ("info", EnterpriseInfoForm),
    ("login", CredentialsForm),
    ("contact", ContactForm),
    ("pfp", ProfilePicForm),
]

TEMPLATE = {
    "general_form": "enterprise.html"
}

class RegisterWizardView(SessionWizardView):
    # Serve pro wizard salvar os arquivos temporariamente
    label_suffix = ""
    file_storage = FileSystemStorage()
    form_list = FORMS

    def get_template_names(self):
        return ['enterprise.html']

    def done(self, form_list, **kwargs):
        data = {}
        for form in form_list:
            if hasattr(form, 'cleaned_data'):
                data.update(form.cleaned_data)

        # Cria o usuário
        user = User.objects.create(
            email=data.get('email'),
            profile_picture=data.get('profile_picture', None),
            is_active=False,
            user_role=User.UserRole.ENTERPRISE,
        )
        # Salva a senha com hash
        if data.get('password'):
            user.set_password(data.get('password'))
        user.save()

        # Cria a empresa 
        enterprise = Enterprise.objects.create(
            user=user,
            corporate_reason=data.get('corporate_reason', ''),
            trade_name=data.get('trade_name', ''),
            cnpj=data.get('cnpj', ''),
            line_of_business=data.get('line_of_business', ''),
            description=data.get('description', ''),
        )

        # Cria o endereço
        if data.get('cep') or data.get('street_name'):
            address = Address.objects.create(
                user=user,
                cep=data.get('cep', ''),
                city=data.get('city', ''),
                state=data.get('state', ''),
                neighborhood=data.get('neighborhood', ''),
                street_name=data.get('street_name', ''),
                number=data.get('number', ''),
                complement=data.get('complement', ''),
            )
            address.save()

        # Cria o telefone 
        if data.get('phone_number'):
            phone = Phone.objects.create(
                phone_number=data.get('phone_number'),
                phone_type=Phone.PhoneType.MOBILE,
                user=user,
            )
            phone.save()

        if data.get('phone_number2'):
            phone = Phone.objects.create(
                phone_number=data.get('phone_number2'),
                phone_type=Phone.PhoneType.OTHER,
                user=user,
            )
            phone.save()

        enterprise.save()
        return redirect('register_done')


class RegisterDoneView(TemplateView):
    template_name = 'done.html'
    
    
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
