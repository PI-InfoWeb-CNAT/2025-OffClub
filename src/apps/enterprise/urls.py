from django.urls import path, include
from .views import *
urlpatterns = [
    path("enterprise_register/", RegisterWizardView.as_view(FORMS), name="enterprise_register")
]