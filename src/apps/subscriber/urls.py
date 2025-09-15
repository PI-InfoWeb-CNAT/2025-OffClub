from django.urls import path, include
from .views import HistoryView

urlpatterns = [
    path('history/', HistoryView.as_view(), name='history')
]