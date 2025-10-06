from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, TemplateView
from django.core.files.storage import FileSystemStorage
from .forms import (
    EnterpriseInfoForm,
    CredentialsForm,
    ContactForm,
    ProfilePicForm,
    LoginForm
)
from formtools.wizard.views import SessionWizardView
from apps.users.models import User
from .models import Enterprise
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

class EnterpriseViews(View):
    @staticmethod
    def enterprise_register(request):
        if request.method == 'GET':
            context = {
                "hello": "world"
            }
            return render(request, "enterprise.html", context=context)


class RegisterWizardView(SessionWizardView):
    # Serve pro wizard salvar os arquivos temporariamente
    file_storage = FileSystemStorage()
    form_list = FORMS

    def get_template_names(self):
        return [TEMPLATE[self.steps.current_step]]

    def done(self, form_list, **kwargs):
        # Junta os dados limpos de todos os forms em um único dict
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
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            cpf=data.get('cpf', ''),
        )

        # Cria o endereço se estiver presente 
        # (Não tenho certeza se é obrigatório)
        if data.get('cep') or data.get('street_name'):
            address = Address.objects.create(
                user=user,
                cep=data.get('cep', ''),
                city=data.get('city', ''),
                uf=data.get('uf', ''),
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

        enterprise.save()
        return redirect('enterprise:registration_done')


class RegisterDone(TemplateView):
    template_name = 'submmited.html'