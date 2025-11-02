from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('subscription/', include('apps.subscription.urls')),
    path('subscriber/', include('apps.subscriber.urls')),
    path('enterprise/', include('apps.enterprise.urls')),
    path('adm_user/', include('apps.admin_user.urls')),
    path('offer/', include('apps.offer.urls')),
]
