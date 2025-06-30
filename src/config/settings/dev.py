from .base import *

# TODO definir uma chave secreta de desenvolvimento
SECRET_KEY = 'not_secret_key_development'

DEBUG = True

ALLOWED_HOSTS += [
    "*",
]

MIDDLEWARE += []

INSTALLED_APPS += []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
