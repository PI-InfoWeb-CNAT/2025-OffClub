from django.db.models import Avg, Count
from apps.subscriber.models import Evaluation

class SeeEvaluationsService():

    def evaluation_stats(coupon_id): 
        evaluations = Evaluation.objects.filter(coupon_id=coupon_id)
        total = evaluations.count()

        if total == 0:
            return {
                "media": 0,
                "total": 0,
                "percentages": {i: 0 for i in range(1, 6)}   # cria um dicionário com todas as avaliações zeradas
            }

        # Média das estrelas
        media = evaluations.aggregate(avg_stars=Avg("stars"))["avg_stars"]

        # Contagem por quantidade de estrelas
        count_by_stars = (
            evaluations.values("stars")             # agrupa os resultados pela quant de estrelas, retornando uma lista de dicionários
            .annotate(count=Count("stars"))         # quantas avaliações tem para cada quant de estrelas
            .order_by("-stars")
        )

        # Cálculo das porcentagens
        percentages = {i: 0 for i in range(1, 6)}   # cria um dicionário com todas as avaliações 
        for n in count_by_stars:
            star = n["stars"]         # atualiza os valores do dicionário
            count = n["count"]
            percentages[star] = round((count / total) * 100, 1)

        return {
            "media": round(media, 1),
            "total": total,
            "percentages": percentages
        }
