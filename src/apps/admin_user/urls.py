from django.urls import path, include
from .views import *

app_name = 'admin_user'

urlpatterns = [
    path('enterprises_requests/', EnterpriseRequestsView.as_view(), name='enterprises_requests'),
    path('enterprises_requests/<uuid:pk>/', EnterpriseRequestDetailView.as_view(), name='enterprise_request_detail'),
    path('request/process/<uuid:pk>/', EnterpriseRequestProcessView.as_view(), name='process_enterprise_request'),
]