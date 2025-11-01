from django.urls import path, include
from .views import EnterpriseDashboardView

urlpatterns = [
    path('dashboard/', EnterpriseDashboardView.as_view(), name='enterprise_dashboard'),
]