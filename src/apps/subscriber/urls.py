from django.urls import path, include
from .views import HistoryView, RegisterWizardView

# TODO: Adicionar namespaces dos outros app
app_name = 'subscriber' # Namespace (namespace:url_name)

urlpatterns = [
    path('register/', RegisterWizardView.as_view(), name='register'),
    path('history/', HistoryView.as_view(), name='history')
]