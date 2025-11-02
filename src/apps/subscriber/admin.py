from django.contrib import admin
from .models import Subscriber, Evaluation

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cpf', 'user_email')
    search_fields = ('first_name', 'last_name', 'cpf', 'user__email')
    ordering = ('first_name', 'last_name')

    @admin.display(description='E-mail do Usuário', ordering='user__email')
    def user_email(self, obj):
        return obj.user.email


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = (
        'coupon',
        'stars',
        'message'
    )
    ordering = ('coupon', '-stars')
    list_filter = ('coupon', 'stars')
    search_fields = ('coupon', 'stars')