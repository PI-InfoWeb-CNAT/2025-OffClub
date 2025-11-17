from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('subscription/', include('apps.subscription.urls')),
    path('subscriber/', include('apps.subscriber.urls')),
    path('enterprise/', include('apps.enterprise.urls')),
    path('adm_user/', include('apps.admin_user.urls')),
    path('offer/', include('apps.offer.urls')),

    # redireciona para offer:manage_list(Para não alterar o template na offer feito por clara)
    path(
        'offer/list/',
        RedirectView.as_view(pattern_name='offer:manage_list', permanent=False),
        name='offer_list'
    ),
    path('coupon/', include(('apps.coupon.urls'), namespace='coupon')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
