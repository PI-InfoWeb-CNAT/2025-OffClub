from django.contrib import admin
from .models import *

# Register your models here.
class OfferAdmin(admin.ModelAdmin):
    list_display = ('name', 'enterprise',)
    empty_value_display = ' - '

admin.site.register(Offer, OfferAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    empty_value_display = ' - '

admin.site.register(Category, CategoryAdmin)