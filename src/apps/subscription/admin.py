from django.contrib import admin
from .models import SubscriptionPlan, Subscription, Feature
from .forms import SubscriptionPlanForm

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    form = SubscriptionPlanForm

    list_display = ('title', 'description', 'price', 'duration')
    search_fields = ('title', 'description', 'features__name')
    list_filter = ('price', 'features')
    ordering = ('title', 'price')
    

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active')
    search_fields = ('user__username', 'plan__title')
    list_filter = ('start_date', 'end_date')
    ordering = ('-start_date',)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'plan')