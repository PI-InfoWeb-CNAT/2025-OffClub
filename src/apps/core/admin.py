from django.contrib import admin
from .models import Phone

@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'phone_type', 'user')
    list_filter = ('phone_type',)
    search_fields = ('phone_number', 'user__email')
    empty_value_display = ' - '

