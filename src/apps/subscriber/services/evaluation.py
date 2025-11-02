from apps.subscriber.models import Evaluation

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
