from django.contrib import admin
from .models import Offer, Category

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'enterprise',
        'category',
        'price',
        'discount',
        'final_price',
        'display_is_active',
        'end_date',
    )

    search_fields = ('title', 'description', 'enterprise__trade_name')

    list_filter = ('category', 'start_date', 'end_date', 'enterprise')

    fieldsets = (
        ('Informações Principais', {
            'fields': ('title', 'enterprise', 'category', 'description', 'image')
        }),
        ('Valores', {
            'fields': ('price', 'discount')
        }),
        ('Datas e Prazos', {
            'fields': ('start_date', 'end_date', 'redemption_period')
        }),
    )
    
    empty_value_display = ' - '

    @admin.display(description='Está Ativa?', boolean=True)
    def display_is_active(self, obj):
        return obj.is_active

    @admin.display(description='Preço Final')
    def final_price(self, obj):
        if obj.discount > 0:
            final_price = float(obj.price) * (1 - float(obj.discount) / 100)
            return f"R$ {final_price:.2f}"
        return f"R$ {obj.price:.2f}"
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',) 
    empty_value_display = ' - '