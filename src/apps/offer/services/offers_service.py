from ..models import Offer, Category
from django.utils import timezone
from django.core.paginator import Paginator

class OfferService():
    @staticmethod
    def list_filter_offer(name, filter_min_discount, pageNum, filter_categories):
        """
        Filtra ofertas e retorna o contexto completo para o template,
        mantendo os dados como QuerySet para paginação eficiente.

        Observação: o filtro por datas foi removido — apenas ofertas ativas são consideradas.
        """
        offers_queryset = Offer.objects.filter(end_date__gte=timezone.now()).select_related('enterprise__user', 'category').order_by('-start_date')

        if name:
            offers_queryset = offers_queryset.filter(title__icontains=name)
        if filter_min_discount:
            offers_queryset = offers_queryset.filter(discount__gte=filter_min_discount)
        if filter_categories:
            offers_queryset = offers_queryset.filter(category_id__in=filter_categories)
        
        paginator = Paginator(offers_queryset, 8)
        page_obj = paginator.get_page(pageNum) 

        # Apenas categorias que tenham ao menos uma oferta ativa
        categories = Category.objects.filter(offers__end_date__gte=timezone.now()).distinct()
        cheap_offers = Offer.objects.filter(end_date__gte=timezone.now()).order_by('price')[:7]

        context = {
            'page_obj': page_obj, 
            'offersCount': paginator.count,
            'cheapOffers': cheap_offers,
            'categories': categories,
        }
        
        return context

    @staticmethod
    def final_price(price, discount_percentage):
        if discount_percentage > 0:
            final_price = float(price) - (float(price) * float(discount_percentage) /100)
            final_price = ("%.2f" % final_price)
        return price, final_price
    
    