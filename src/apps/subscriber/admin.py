from django.contrib import admin
from .models import *

# Register your models here.

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    empty_value_display = ' - '

admin.site.register(Subscriber, SubscriberAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    empty_value_display = ' - '

admin.site.register(Subscription, SubscriptionAdmin)