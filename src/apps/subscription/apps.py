from django.apps import AppConfig


class SubscriptionConfig(AppConfig): #type: ignore
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.subscription'