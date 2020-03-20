"""
This is the settings file used in production.
First, it imports all default settings, then overrides respective ones.
Secrets are stored in and imported from an additional file, not set under version control.
"""

from corona import settings_secrets as secrets
from corona.settings import *

SECRET_KEY = secrets.SECRET_KEY

DEBUG = False

ALLOWED_HOSTS = ['deutschlandzusammen.de', 'www.deutschlandzusammen.de']

HOST_NAME = 'https://www.deutschlandzusammen.de'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'koronadb',
        'USER': 'koronadb',
        'PASSWORD': secrets.DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

STATIC_ROOT = '/var/www/virtual/korona/html/static'

GDAL_LIBRARY_PATH = '/home/korona/lib/libgdal.so'
GEOS_LIBRARY_PATH = '/home/korona/lib/libgeos_c.so'

MAPBOX_API_TOKEN = secrets.MAPBOX_API_TOKEN

EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@deutschlandzusammen.de'
EMAIL_HOST_PASSWORD = secrets.EMAIL_PASSWORD
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

WEBPUSH_SETTINGS = {
    'VAPID_PUBLIC_KEY': secrets.VAPID_PUBLIC_KEY,
    'VAPID_PRIVATE_KEY': secrets.VAPID_PRIVATE_KEY,
    'VAPID_ADMIN_EMAIL': 'support@deutschlandzusammen.de'
}
