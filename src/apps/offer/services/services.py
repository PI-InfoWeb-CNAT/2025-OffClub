from ..models import Offer
from django.utils import timezone

class OfferService():
    @staticmethod
    def final_price(price, discount_percentage):
        if discount_percentage > 0:
            final_price = float(price) - (float(price) * float(discount_percentage) /100)
            final_price = ("%.2f" % final_price)
        return price, final_price
    @staticmethod
    def list_filter_offer(name, filter_min_discount, filter_start_date, filter_end_date):
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