from django.contrib import admin

# Register your models here.
from .models import SubscriptionPlan

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    empty_value_display = ' - '

admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)