from django.contrib import admin
from .models import *

# Register your models here.
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('trade_name', 'corporate_reason',)
    empty_value_display = ' - '

admin.site.register(Enterprise, EnterpriseAdmin)

class OperationAreaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    empty_value_display = ' - '

admin.site.register(OperationArea, OperationAreaAdmin)