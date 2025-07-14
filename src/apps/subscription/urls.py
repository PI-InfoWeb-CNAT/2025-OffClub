from django.urls import path, include
from .views import PlansViews

urlpatterns = [
    path('plans/', PlansViews.plans, name='plans'),
]