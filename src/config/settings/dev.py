from .base import *

# TODO definir uma chave secreta de desenvolvimento
SECRET_KEY = 'not_secret_key_development'

DEBUG = True

ALLOWED_HOSTS += [
    "*",
]

MIDDLEWARE += []

INSTALLED_APPS += [
    'apps.coupon',
    'apps.enterprise',
    'apps.offer',
    'apps.core',
    'apps.subscriber',
    'apps.subscription',
    'apps.users',
    'apps.admin_user'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LOGIN_URL = "/subscriber/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

