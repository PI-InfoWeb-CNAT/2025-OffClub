import logging

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView
from django.core.files.storage import FileSystemStorage
from django.db import transaction

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

    def render_done(self, form, **kwargs):
        """Skip revalidation so we can land on done even with invalid steps."""
        final_forms = {}
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key),
            )
            form_obj.is_valid()
            final_forms[form_key] = form_obj

        done_response = self.done(list(final_forms.values()), form_dict=final_forms, **kwargs)
        self.storage.reset()
        return done_response

    def done(self, form_list, **kwargs):
        data = {}
        for form in form_list:
            if hasattr(form, 'cleaned_data'):
                data.update(form.cleaned_data)

        try:
            with transaction.atomic():
                # Cria o usuário
                user = User.objects.create(
                    email=data.get('email'),
                    profile_picture=data.get('profile_picture', None),
                    is_active=False,
                    user_role=User.UserRole.ENTERPRISE,
                )

                # Salva a senha com hash, caso exista
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

                # Cria o endereço, se necessário
                if data.get('cep') or data.get('street_name'):
                    Address.objects.create(
                        user=user,
                        cep=data.get('cep', ''),
                        city=data.get('city', ''),
                        state=data.get('state', ''),
                        neighborhood=data.get('neighborhood', ''),
                        street_name=data.get('street_name', ''),
                        number=data.get('number', ''),
                        complement=data.get('complement', ''),
                    )

                # Cria os telefones, se fornecidos
                if data.get('phone_number'):
                    Phone.objects.create(
                        phone_number=data.get('phone_number'),
                        phone_type=Phone.PhoneType.MOBILE,
                        user=user,
                    )

                if data.get('phone_number2'):
                    Phone.objects.create(
                        phone_number=data.get('phone_number2'),
                        phone_type=Phone.PhoneType.OTHER,
                        user=user,
                    )

                enterprise.save()

        except Exception:
            # Garante o redirecionamento mesmo que a persistência falhe
            logger.exception("Enterprise registration data could not be fully persisted.")

        return redirect('enterprise:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'done.html'
    

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
    template_name = 'enterprise_dashboard.html'
    
    def get(self, request):
        return render(request, 'enterprise_dashboard.html')


# class EnterpriseSignUpView(CreateView):
#     """
#     Renderiza e processa o formulário de registro para novas empresas.
#     """
#     form_class = EnterpriseSignUpForm
#     template_name = 'registration/signup_form.html'
    
#     sucess_url = reverse_lazy('enterprise_signup_done')
    
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'enterprise'
#         return super().get_context_data(**kwargs)
    
# def enterprise_signup_done(request):
#     """
#     Página de sucesso exibida após o registro bem sucedido.
#     """
#     return render(request, 'registration/signup_done.html')
