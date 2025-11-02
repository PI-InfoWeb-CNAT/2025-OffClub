from django.urls import path, include
from .views import *

app_name = 'enterprise'

urlpatterns = [
    path("register/", RegisterWizardView.as_view(FORMS), name="enterprise_register"),
    path("register/success/", RegisterDoneView.as_view(), name="register_done"),
]