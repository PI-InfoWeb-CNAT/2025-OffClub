from django.contrib import admin
from .models import Enterprise, LineOfBusiness

@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('trade_name', 'corporate_reason', 'cnpj', 'user_email')
    search_fields = ('trade_name', 'cnpj', 'corporate_reason')
    list_filter = ('line_of_business',) 

    @admin.display(description='E-mail do Usuário', ordering='user__email')
    def user_email(self, obj):
        return obj.user.email
    

@admin.register(LineOfBusiness)
class LineOfBusinessAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)