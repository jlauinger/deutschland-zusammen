from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from offers.views import AccountRegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register', AccountRegistrationView.as_view(), name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('webpush/', include('webpush.urls')),
    path('metrics/' + settings.PROMETHEUS_PATH_SECRET + '/', include('django_prometheus.urls')),
    path('', include('offers.urls')),
]
