from ...enterprise.models import Enterprise
from ...subscriber.models import Subscriber
from ...offer.models import Category
from django.utils import timezone
from django.core.paginator import Paginator

class AboutService():
    @staticmethod
    def about_page_context():
        count_enterprises = Enterprise.objects.all().count()
        count_subscribers = Subscriber.objects.all().count()

        # categorias e depoimentos para a página sobre
        categories = Category.objects.all()
        testimonials = [
            {
                'rating': 5,
                'text': 'A proposta do OffClub fortalece o comércio local e dá opções reais de economia para quem mora por perto.',
                'author_name': 'Roberto Luiz',
                'author_role': 'Cliente'
            },
            {
                'rating': 5,
                'text': 'Tivemos um aumento de fluxo desde que começamos com os cupons — simples e eficiente.',
                'author_name': 'Patrícia Gomes',
                'author_role': 'Empresária'
            }
        ]

        context = {
            'count_enterprises': count_enterprises,
            'count_subscribers': count_subscribers,
            'categories': categories,
            'testimonials': testimonials
        }
        return context
    