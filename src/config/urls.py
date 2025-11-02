from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('subscription/', include('apps.subscription.urls')),
    path('offer/', include('apps.offer.urls')),
    path('subscriber/', include('apps.subscriber.urls')),
    path('enterprise/', include('apps.enterprise.urls')),
    path('adm_user/', include('apps.admin_user.urls'))
]

from .settings import base as settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
