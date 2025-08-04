from django.apps import AppConfig

class SubscriberConfig(AppConfig): #type: ignore
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.subscriber'