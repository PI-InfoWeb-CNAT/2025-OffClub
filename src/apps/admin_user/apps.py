from django.apps import AppConfig


class Admin_UserConfig(AppConfig): #type: ignore
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.admin_user'