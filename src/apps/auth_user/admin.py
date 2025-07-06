from django.contrib import admin
from .models import *

# Register your models here.
class AuthUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'enterprise',)
    empty_value_display = ' - '

admin.site.register(AuthUser, AuthUserAdmin)