from django.db.models import Avg, Count
from apps.subscriber.models import Evaluation

# class SeeEvaluationsService():

#     def evaluation_stats(coupon_id): 
#         evaluations = Evaluation.objects.filter(coupon_id=coupon_id)
#         total = evaluations.count()

#         if total == 0:
#             return {
#                 "media": 0,
#                 "total": 0,
#                 "percentages": {i: 0 for i in range(1, 6)}   # cria um dicionário com todas as avaliações zeradas
#             }

#         # Média das estrelas
#         media = evaluations.aggregate(avg_stars=Avg("stars"))["avg_stars"]

#         # Contagem por quantidade de estrelas
#         count_by_stars = (
#             evaluations.values("stars")             # agrupa os resultados pela quant de estrelas, retornando uma lista de dicionários
#             .annotate(count=Count("stars"))         # quantas avaliações tem para cada quant de estrelas
#             .order_by("-stars")
#         )

#         # Cálculo das porcentagens
#         percentages = {i: 0 for i in range(1, 6)}   # cria um dicionário com todas as avaliações 
#         for n in count_by_stars:
#             star = n["stars"]         # atualiza os valores do dicionário
#             count = n["count"]
#             percentages[star] = round((count / total) * 100, 1)

#         return {
#             "media": round(media, 1),
#             "total": total,
#             "percentages": percentages
#         }

class SeeEvaluationsService:

    @staticmethod
    def final_price(price, discount):
        return round(price * (1 - discount / 100), 2)
    
    @staticmethod
    def get_evaluations(coupon):
        """Pega todas as avaliações e ordena pela quantidade de estrela"""

        return Evaluation.objects.filter(coupon=coupon).order_by("-stars")
    
    @staticmethod
    def evaluation_stats(coupon):
        evaluations = Evaluation.objects.filter(coupon=coupon)
        total = evaluations.count()

        if total == 0:
            return{
                "media": 0,
                "total": 0,
                "quantity_by_stars": {i: 0 for i in range(1, 6)},
                "percentages": {i: 0 for i in range(1, 6)},
            }
        
        # Média das avaliações
        media = evaluations.aggregate(media=Avg("stars"))["media"]

        # Quantidade de avaliações por estrelas
        quantity_by_stars = (
            evaluations.values("stars")          # agrupa os resultados pela quant de estrelas, retornando uma lista de dicionários
            .annotate(count=Count("stars"))      # quantas avaliações tem para cada quant de estrelas
            .order_by("-stars")
        )
        dict_quantity = {
            i: 0 for i in range(1, 6)
        }
        for s in quantity_by_stars:              # atualiza os valores 
            dict_quantity[s["stars"]] = s["count"] 

        # Cálculo das porcentagens
        percentages = {
            star: round((count / total) * 100, 1)
            for star, count in dict_quantity.items()
        }

        return {
            "media": media,
            "total": total,
            "quantity_by_stars": quantity_by_stars,
            "percentages": percentages
        }