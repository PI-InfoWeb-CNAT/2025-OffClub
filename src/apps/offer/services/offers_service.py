from ..models import Offer, Category
from django.utils import timezone
from django.core.paginator import Paginator

class OfferService():
    @staticmethod
    def list_filter_offer(name, filter_min_discount, filter_start_date, filter_end_date, pageNum, filter_categories):
        """
        Filtra ofertas e retorna o contexto completo para o template,
        mantendo os dados como QuerySet para paginação eficiente.
        """
        offers_queryset = Offer.objects.filter(end_date__gte=timezone.now()).select_related('enterprise__user', 'category').order_by('-start_date')

        if name:
            offers_queryset = offers_queryset.filter(title__icontains=name)
        if filter_min_discount:
            offers_queryset = offers_queryset.filter(discount__gte=filter_min_discount)
        if filter_start_date:
            offers_queryset = offers_queryset.filter(start_date__gte=filter_start_date)
        if filter_end_date:
            offers_queryset = offers_queryset.filter(end_date__lte=filter_end_date)
        if filter_categories:
            offers_queryset = offers_queryset.filter(category_id__in=filter_categories)
        
        paginator = Paginator(offers_queryset, 8)
        page_obj = paginator.get_page(pageNum) 

        categories = Category.objects.all()
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
    
    