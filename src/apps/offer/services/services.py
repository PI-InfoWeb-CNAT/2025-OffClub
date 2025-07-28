from ..models import Offer, Category
from django.utils import timezone
from django.core.paginator import Paginator

class OfferService():
    @staticmethod
    def list_filter_offer(name, filter_min_discount, filter_start_date, filter_end_date, pageNum, filter_categories):
        categories = Category.objects.all()
        offers = OfferService.filter_offer(name, filter_min_discount, filter_start_date, filter_end_date, filter_categories)
        cheapOffers = OfferService.cheap_offers()
        offersCount = offers.__len__()

        offersPaginator = Paginator(offers, 8)
        if pageNum  == None:
            pageNum = 1
        
        page = offersPaginator.get_page(pageNum)
        startNum = (int(pageNum) - 1)*8 + 1
        endNum = int(pageNum) * 8

        pages = []
        p = 1
        while p <= offersPaginator.num_pages:
            pages.append(str(p))
            p = p + 1

        context = {'page' : page, 'pageNum': str(pageNum), 'endNum': endNum, 'startNum': startNum, 'offersCount': offersCount, 'cheapOffers' : cheapOffers, 'pages': pages, 'categories': categories}
        return context

    @staticmethod
    def final_price(price, discount_percentage):
        if discount_percentage > 0:
            final_price = float(price) - (float(price) * float(discount_percentage) /100)
            final_price = ("%.2f" % final_price)
        return price, final_price
    
    @staticmethod
    def filter_offer(name, filter_min_discount, filter_start_date, filter_end_date, filter_categories):
        allObjects = Offer.objects.filter(end_date__gte=timezone.now())
        filteredObjects = allObjects

        if name:
            filteredObjects = filteredObjects.filter(title__icontains=name)
        if filter_min_discount:
            filteredObjects = filteredObjects.filter(discount__gte=filter_min_discount)
        if filter_start_date:
            if filter_end_date:
                filteredObjects = filteredObjects.filter(end_date__range=(filter_start_date, filter_end_date))
            else:
                filteredObjects = filteredObjects.filter(end_date__gte=filter_start_date)
        elif filter_end_date:
            filteredObjects = filteredObjects.filter(end_date__lte=filter_end_date)
        if filter_categories:
            filteredObjects = filteredObjects.filter(category_id__in=filter_categories)

        offers = []

        for offer in filteredObjects:
            price = offer.price
            discount = offer.discount
            old_price, final_price = OfferService.final_price(price, discount)
            price_data = {
                    'old_price':     old_price,
                    'final_price':   final_price,
                }
            dic = {'object': offer, 'data': price_data}
            offers.append(dic)

        return offers
    
    @staticmethod
    def cheap_offers():
        allObjects = Offer.objects.filter(end_date__gte=timezone.now())
        
        cheapObjects = allObjects.order_by('price')[:7]
        cheapOffers = []

        for offer in cheapObjects:
            price = offer.price
            discount = offer.discount
            old_price, final_price = OfferService.final_price(price, discount)
            price_data = {
                    'old_price':     old_price,
                    'final_price':   final_price,
                }
            dic = {'object': offer, 'data': price_data}
            cheapOffers.append(dic)

        return cheapOffers