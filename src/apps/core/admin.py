from django.contrib import admin
from .models import *

# Register your models here.
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('number', 'type',)
    empty_value_display = ' - '

admin.site.register(Phone, PhoneAdmin)