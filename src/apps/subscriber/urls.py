from django.urls import path, include
from .views import HistoryView

# TODO: Adicionar namespaces dos outros app
app_name = 'subscriber' # Namespace 

urlpatterns = [
    path('history/', HistoryView.as_view(), name='history')
]