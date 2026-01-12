from django.urls import path
from .views import (
    EvaluationCreateView,
    HistoryView,
    LoginView,
    RegisterWizardView,
    RegistrationDone,
    ProfileView,
    EditProfileView,
    MyPlansView,
)
from django.contrib.auth.views import LogoutView

# TODO: Adicionar namespaces dos outros app
app_name = 'subscriber' # Namespace (namespace:url_name)

urlpatterns = [
    path('register/', RegisterWizardView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('history/', HistoryView.as_view(), name='history'),
    path('registration_done/', RegistrationDone.as_view(), name='registration_done'),
    path('avaliar_cupom/<uuid:coupon_id>/', EvaluationCreateView.as_view(), name='evaluate_coupon'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/plans/', MyPlansView.as_view(), name='my_plans'),
]
