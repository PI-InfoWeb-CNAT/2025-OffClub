from django.urls import path, include
from .views import HistoryView, RegisterWizardView, LoginView
from django.contrib.auth.views import LogoutView

# TODO: Adicionar namespaces dos outros app
app_name = 'subscriber' # Namespace (namespace:url_name)

urlpatterns = [
    path('register/', RegisterWizardView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('history/', HistoryView.as_view(), name='history')
]