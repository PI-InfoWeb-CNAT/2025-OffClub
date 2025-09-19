from django.shortcuts import render
from django.views.generic import ListView, CreateView
from apps.coupon.models import Coupon
from apps.users.forms import SubscriberSignUpForm

def calculate_discount(price, discount_percentage):
    """Calcula o preço final após aplicar um desconto percentual."""
    final_price = price - (price * discount_percentage / 100)
    return price, final_price


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
  
            old_price, final_price = calculate_discount(price, discount)
            
            coupon_data = {
                'old_price': old_price,
                'final_price': final_price,
            }
  
            processed_coupons.append({'object': coupon, 'data': coupon_data})

        context['coupons'] = processed_coupons
        
        return context


class SubscriberSignUpView(CreateView):
    """
    Renderiza e processa o formulário de registro para novos assinantes.
    """
    form_class = SubscriberSignUpForm
    template_name = 'registration/signup_form.html'
    success_url = '/'
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'subscriber'
        return super().get_context_data(**kwargs)