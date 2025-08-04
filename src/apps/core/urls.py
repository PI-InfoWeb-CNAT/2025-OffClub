from django.urls import path, include
from .views import HomeViews

urlpatterns = [
    path('', view=HomeViews.as_view(), name='home'),
]