from django.shortcuts import render
from .services.about_service import AboutService
from django.views import View

from apps.offer.models import Category
from apps.subscription.models import SubscriptionPlan, Feature, Subscription as UserSubscription
from django.utils import timezone


class HomeViews(View):
    template_name = 'home.html'
    
    def get(self, request):
        # Categorias para o slider de categorias
        categories = Category.objects.all()

        # Planos e features para exibição dinâmica na home
        plans = SubscriptionPlan.objects.all()
        all_features = Feature.objects.all()

        # Assinatura ativa do usuário, se houver
        active_subscription = None
        if request.user.is_authenticated:
            subs = UserSubscription.objects.filter(user=request.user).order_by('-start_date')
            for s in subs:
                if s.is_active:
                    active_subscription = s
                    break

        # Depoimentos estáticos para a home
        testimonials = [
            {
                'rating': 5,
                'text': 'Encontrei ofertas reais de empresas locais e economizei bastante. A plataforma é intuitiva e segura.',
                'author_name': 'Mariana Silva',
                'author_role': 'Cliente'
            },
            {
                'rating': 5,
                'text': 'Como comerciante, percebi aumento de clientes graças aos cupons. Funcionou muito bem para o meu negócio.',
                'author_name': 'Carlos Pereira',
                'author_role': 'Empresário'
            },
            {
                'rating': 4,
                'text': 'A interface é agradável e os planos atendem às necessidades. Recomendo para quem quer apoiar o comércio local.',
                'author_name': 'Ana Costa',
                'author_role': 'Cliente'
            }
        ]

        context = {
            'categories': categories,
            'plans': plans,
            'all_features': all_features,
            'active_subscription': active_subscription,
            'testimonials': testimonials
        }

        return render(request, 'home.html', context=context)

class AboutViews(View):
    template_name = 'about.html'
    
    def get(self, request):
        context = AboutService.about_page_context()
        return render(request, 'about.html', context = context)
        
