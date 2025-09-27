from django.urls import path, include
from .views import EnterpriseViews
urlpatterns = [
    path("enterprise_register/", EnterpriseViews.enterprise_register, name="enterprise_register")
]