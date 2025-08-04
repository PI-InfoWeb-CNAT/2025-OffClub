from django.urls import path, include
from .views import home

urlpatterns = [
    path('', view=home, name='home'),
]