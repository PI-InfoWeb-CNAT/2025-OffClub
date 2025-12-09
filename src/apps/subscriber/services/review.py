from apps.subscriber.models import Review


class ReviewService:
    @staticmethod
    def create_review(coupon, stars, message=""):
        """Cria uma nova avaliação para o cupom informado."""

        return Review.objects.create(
            coupon=coupon,
            stars=stars,
            message=message,
        )
