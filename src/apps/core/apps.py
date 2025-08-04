from django.apps import AppConfig


class CoreConfig(AppConfig): #type: ignore
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'