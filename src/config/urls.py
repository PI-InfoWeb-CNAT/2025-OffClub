from django.contrib import admin
from django.urls import path, include
from apps.core import urls as core_urls
from apps.subscription.urls import urlpatterns as subscription_urls
from apps.offer.urls import urlpatterns as offers_urls
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(core_urls)),
    path('subscription/', include(subscription_urls)),
    path('offers/', include(offers_urls)),
]
