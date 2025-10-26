from ..models import Evaluation    

class ServiceDiscount():
    @staticmethod
    def final_price(price, discount_percentage):
        if discount_percentage > 0:
            final_price = float(price) - (float(price) * float(discount_percentage) /100)
        return price, final_price

class EvaluationService():
    def create_evaluation(coupon, stars, message="", ):
        """
        Cria uma avaliação para cada cupom.
        """

        evaluation = Evaluation.objects.create(
            coupon=coupon,
            stars=stars,
            message=message
        )

        return evaluation
