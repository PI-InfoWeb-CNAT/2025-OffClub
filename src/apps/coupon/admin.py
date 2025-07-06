from django.contrib import admin

# Register your models here.
from .models import Coupon

class CouponAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    list_display = ('subscriber', 'offer', 'code')
    empty_value_display = ' - '

admin.site.register(Coupon, CouponAdmin)