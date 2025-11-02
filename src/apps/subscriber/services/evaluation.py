from apps.subscriber.models import Evaluation


class EvaluationService:
    @staticmethod
    def create_evaluation(coupon, stars, message=""):
        """Cria uma nova avaliação para o cupom informado."""

        return Evaluation.objects.create(
            coupon=coupon,
            stars=stars,
            message=message,
        )
