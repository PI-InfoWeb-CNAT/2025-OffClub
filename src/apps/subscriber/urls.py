from django.urls import path, include
from .views import HistoryView, RegisterWizardView, LoginView, RegistrationDone
from django.contrib.auth.views import LogoutView
from .views import SubscriberViews, EvaluationCreateView

# TODO: Adicionar namespaces dos outros app
app_name = 'subscriber' # Namespace (namespace:url_name)

urlpatterns = [
    path('register/', RegisterWizardView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('history/', HistoryView.as_view(), name='history'),
    path('registration_done/', RegistrationDone.as_view(), name='registration_done'),
    path('historico_consumo/', SubscriberViews.consumption_history_list, name='history'),
    path('avaliar_cupom/<uuid:coupon_id>/', EvaluationCreateView.as_view(), name='evaluate_coupon'),
]
