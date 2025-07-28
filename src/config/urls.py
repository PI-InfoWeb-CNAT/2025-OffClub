from django.contrib import admin
from django.urls import path, include
from apps.core import urls as core_urls
from apps.subscription.urls import urlpatterns as subscription_urls
from apps.offer.urls import urlpatterns as offer_urls
from apps.subscriber.urls import urlpatterns as subscriber_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(core_urls)),
    path('subscription/', include(subscription_urls)),
    path('offer/', include(offer_urls)),
    path('subscriber/', include(subscriber_urls)),
]


from .settings import base as settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)