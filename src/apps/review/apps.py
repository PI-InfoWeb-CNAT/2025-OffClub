from django.apps import AppConfig


class ReviewConfig(AppConfig): #type: ignore
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.review'