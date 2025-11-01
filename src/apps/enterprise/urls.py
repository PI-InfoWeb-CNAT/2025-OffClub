from django.urls import path, include
from .views import *
urlpatterns = [
    path("register/", RegisterWizardView.as_view(FORMS), name="enterprise_register"),
    path("register/success/", RegisterDoneView.as_view(), name="register_done"),
]