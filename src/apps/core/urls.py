from django.urls import path, include
from .views import HomeViews, AboutViews

urlpatterns = [
    path('', view=HomeViews.as_view(), name='home'),
    path('about', view=AboutViews.as_view(), name='about'),
]