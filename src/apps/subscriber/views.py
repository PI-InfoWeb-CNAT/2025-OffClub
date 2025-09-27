from django.shortcuts import redirect, render
from django.views.generic import ListView
from apps.coupon.models import Coupon
from .services.discount import DiscountService
from django.core.files.storage import FileSystemStorage
from .forms import (
    PersonalInfoForm,
    LoginForm,
    ContactForm,
    ProfilePicForm
)
from formtools.wizard.views import SessionWizardView
from apps.users.models import User
from .models import Subscriber
from apps.core.models import Address, Phone


FORMS = [
    ("info", PersonalInfoForm),
    ("login", LoginForm),
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
        # Junta os dados limpos de todos os forms em um único dict
        data = {}
        for form in form_list:
            if hasattr(form, 'cleaned_data'):
                data.update(form.cleaned_data)

        # Cria o usuário
        user = User.objects.create(
            email=data.get('email'),
            profile_picture=data.get('profile_picture', None),
            is_active=True,
            user_role=User.UserRole.SUBSCRIBER,
        )
        # Salva a senha com hash
        if data.get('password'):
            user.set_password(data.get('password'))
        user.save()

        # Cria o assinante 
        subscriber = Subscriber.objects.create(
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

        subscriber.save()
        return redirect('login')


class HistoryView(ListView):
    """
    Exibe o histórico de cupons para o usuário logado.
    """
    model = Coupon  
    template_name = 'subscriber.html'
    context_object_name = 'coupons'   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_coupons = context['coupons']
    
        processed_coupons = []
        for coupon in all_coupons:
            price = coupon.offer.price
            discount = coupon.offer.discount

            old_price, final_price = DiscountService.final_price(price, discount)

            coupon_data = {
                'old_price': old_price,
                'final_price': final_price,
            }
  
            processed_coupons.append({'object': coupon, 'data': coupon_data})

        context['coupons'] = processed_coupons
        
        return context


