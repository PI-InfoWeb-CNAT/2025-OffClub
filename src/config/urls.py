from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('subscription/', include('apps.subscription.urls')),
    path('offer/', include('apps.offer.urls')),
    path('subscriber/', include('apps.subscriber.urls')),
]

<<<<<<< HEAD
=======

>>>>>>> origin/31-implementação-das-telas-do-fluxo-principal-do-cdu-buscar-e-filtrar-ofertas
from .settings import base as settings
from django.conf.urls.static import static

if settings.DEBUG:
<<<<<<< HEAD
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> origin/31-implementação-das-telas-do-fluxo-principal-do-cdu-buscar-e-filtrar-ofertas
