from django.contrib import admin
from django.urls import path, include

from offers.views import AccountRegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register', AccountRegistrationView.as_view(), name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path(r'captcha/', include('captcha.urls')),
    path('', include('offers.urls')),
]
