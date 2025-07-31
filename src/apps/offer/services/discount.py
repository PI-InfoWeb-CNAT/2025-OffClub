from ..models import Offer


class Discount:
    offer = Offer.objects.all()

    def calc_discount(cls):
        price = cls.offer.price
        discount = cls.offer.discount

        d = price * discount

        return d


    def calc_total(cls):
        price = cls.offer.price
        d = cls.calc_discount()

        total = price - d

        return total

