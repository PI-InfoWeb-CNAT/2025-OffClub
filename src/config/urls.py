from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('subscription/', include('apps.subscription.urls')),
    path('subscriber/', include('apps.subscriber.urls', namespace='subscriber')),
    path('offer/', include('apps.offer.urls', namespace='offer')),

    # redireciona para offer:manage_list(Para não alterar o template na offer feito por clara)
    path(
        'offer/list/',
        RedirectView.as_view(pattern_name='offer:manage_list', permanent=False),
        name='offer_list'
    ),
]
