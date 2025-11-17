class DiscountService:
    @staticmethod
    def final_price(price, discount_percentage):
        base_price = float(price)
        discount = float(discount_percentage or 0)
        final_price = base_price - (base_price * discount / 100)
        return round(base_price, 2), round(final_price, 2)

