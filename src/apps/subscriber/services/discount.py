class DiscountService():
    @staticmethod
    def final_price(price, discount_percentage):
        if discount_percentage > 0:
            final_price = float(price) - (float(price) * float(discount_percentage) /100)
        return price, final_price

