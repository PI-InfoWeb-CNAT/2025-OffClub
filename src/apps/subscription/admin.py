from django.contrib import admin
from .models import SubscriptionPlan, Subscription

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'duration')
    search_fields = ('title', 'description')
    list_filter = ('price',)
    ordering = ('title',)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('id')
    
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'active')
    search_fields = ('user__username', 'plan__title')
    list_filter = ('active', 'start_date', 'end_date')
    ordering = ('-start_date',)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'plan')