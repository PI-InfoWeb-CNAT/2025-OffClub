from django.urls import path, include
from .views import *
urlpatterns = [
    path('enterprises_requests/', EnterpriseRequestsView.as_view(), name='enterprises_requests'),
    path('enterprises_requests/<uuid:pk>/', EnterpriseRequestDetailView.as_view(), name='enterprise_request_detail'),
]