from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable, Optional, Tuple, Dict, Any
from uuid import UUID

from django.db import transaction
from django.db.models import F, QuerySet, ExpressionWrapper, DecimalField, Value
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.core.paginator import Paginator

from ..models import Offer, Category


class ManageOffer:
    @staticmethod
    def list_filter_offer(
        name: Optional[str] = None,
        filter_min_discount: Optional[float | int | Decimal] = None,
        filter_start_date: Optional[str | Any] = None,
        filter_end_date: Optional[str | Any] = None,
        pageNum: Optional[int | str] = 1,
        filter_categories: Optional[Iterable[int | str]] = None,
        per_page: int = 8,
        only_active: bool = True,
    ) -> Dict[str, Any]:
        now = timezone.now()
        qs: QuerySet[Offer] = (
            Offer.objects.select_related("category").order_by("-start_date")
        )

        if only_active:
            qs = qs.filter(end_date__gte=now)

        if name:
            qs = qs.filter(title__icontains=name)  # campo correto é 'title'

        if filter_min_discount not in (None, "", 0):
            qs = qs.filter(discount__gte=filter_min_discount)

        # Filtrando por datas usando a parte de date para aceitar inputs "YYYY-MM-DD"
        if filter_start_date:
            qs = qs.filter(start_date__date__gte=str(filter_start_date))

        if filter_end_date:
            qs = qs.filter(end_date__date__lte=str(filter_end_date))

        if filter_categories:
            qs = qs.filter(category_id__in=list(filter_categories))

        # Anotação com alias diferente para não colidir com a @property final_price
        discount = Coalesce(F("discount"), Value(0))
        final_price_expr = ExpressionWrapper(
            F("price") * (Value(Decimal("1")) - discount / Value(Decimal("100"))),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        )
        qs = qs.annotate(final_price_ann=final_price_expr)

        paginator = Paginator(qs, per_page)
        page_obj = paginator.get_page(pageNum)

        categories = Category.objects.all()

        cheap_offers = (
            Offer.objects.filter(end_date__gte=now)
            .annotate(final_price_ann=final_price_expr)
            .order_by("final_price_ann")[:7]
        )

        return {
            "page_obj": page_obj,
            "offersCount": paginator.count,
            "cheapOffers": cheap_offers,
            "categories": categories,
        }

    @staticmethod
    def final_price(
        price: Decimal | float | int,
        discount_percentage: Decimal | float | int
    ) -> Tuple[Decimal, Decimal]:
        price = Decimal(str(price))
        discount_percentage = Decimal(str(discount_percentage or 0))
        final_price = price * (Decimal("1") - (discount_percentage / Decimal("100")))
        return price, final_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @staticmethod
    def get_queryset_base() -> QuerySet[Offer]:
        return Offer.objects.select_related("category")

    @staticmethod
    def get(pk: UUID) -> Offer:
        return ManageOffer.get_queryset_base().get(pk=pk)

    @staticmethod
    @transaction.atomic
    def create(data: Dict[str, Any]) -> Offer:
        offer = Offer(**data)
        offer.full_clean()
        offer.save()
        return offer

    @staticmethod
    @transaction.atomic
    def update(offer: Offer, data: Dict[str, Any]) -> Offer:
        for k, v in data.items():
            setattr(offer, k, v)
        offer.full_clean()
        offer.save()
        return offer

    @staticmethod
    @transaction.atomic
    def delete(offer: Offer) -> None:
        offer.delete()

    @staticmethod
    def list_active() -> QuerySet[Offer]:
        now = timezone.now()
        return (
            Offer.objects.filter(end_date__gte=now)
            .select_related("category")
            .order_by("-start_date")
        )

    @staticmethod
    def list_by_category(category_id: int) -> QuerySet[Offer]:
        return (
            Offer.objects.filter(category_id=category_id)
            .select_related("category")
            .order_by("-start_date")
        )
