from django.contrib import admin
from .models import Coupon, Evaluation

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'subscriber',
        'offer_title',
        'offer_discount', 
        'is_active',      
        'expiration_date'
    )
    ordering = ('-creation_date',)

    list_filter = ('offer__enterprise', 'used_date')
    
    search_fields = ('code', 'subscriber__first_name', 'offer__title')
    
    @admin.display(description='Oferta', ordering='offer__title')
    def offer_title(self, obj):
        return obj.offer.title

    @admin.display(description='Desconto (%)', ordering='offer__discount')
    def offer_discount(self, obj):
        return f"{obj.offer.discount}%"
    
    @admin.display(boolean=True, description='Ativo?', ordering='expiration_date')
    def is_active(self, obj):
        return obj.is_active

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = (
        'coupon',
        'stars',
        'message'
    )
    ordering = ('coupon', '-stars')

    list_filter = ('coupon', 'stars')
    
    search_fields = ('coupon', 'stars')