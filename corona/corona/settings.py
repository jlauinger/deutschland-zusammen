"""
Django settings for corona project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.utils.translation import gettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'tm4nzh33&pt64sp_wsmir02w7j1da=jf+6f$i2xpnn+m8or948'

DEBUG = True

ALLOWED_HOSTS = []

HOST_NAME = 'http://localhost:8000'

# Application definition

INSTALLED_APPS = [
    'offers',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'bootstrap4',
    'captcha',
    'webpush',
    'django_prometheus',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'corona.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'offers.context_preprocessors.vapid_key',
                'offers.context_preprocessors.hostname',
            ],
        },
    },
]

WSGI_APPLICATION = 'corona.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gis',
        'USER': 'gis',
        'PASSWORD': 'changeme1',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'de'

LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# Geography settings

SRID = 4326

NOMINATIM_USER_AGENT = "corona-hilfsangebote"
MAPBOX_API_TOKEN = "pk.eyJ1IjoiamxhdWluZ2VyIiwiYSI6ImNrN3RzMWcyNjB3Z3IzbXFyZmZianRkZzAifQ.P0LQjvZ7G0dB9uNqs2r3YQ"

# Auth settings

LOGIN_REDIRECT_URL = '/profile'
LOGOUT_REDIRECT_URL = '/'

# Contact mail settings

EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

CONTACT_MAIL_FROM = 'noreply@deutschlandzusammen.de'
CONTACT_MAIL_SUBJECT = _('Neue Nachricht von deutschlandzusammen.de')
CONTACT_MAIL_BODY = _("""Hallo {}!

Du hast eine neue Anfrage nach Hilfe über deutschlandzusammen.de!

Daten zur suchenden Person:
Name: {}
E-Mail: {}
Telefon: {}

Nachricht:
{}

Melde dich doch wenn du kannst schnellstmöglich zurück.

Liebe Grüße
dein Team von deutschlandzusammen.de
""")

ACTIVATION_MAIL_FROM = 'noreply@deutschlandzusammen.de'
ACTIVATION_MAIL_SUBJECT = _('Aktiviere deinen Account bei deutschlandzusammen.de')
ACTIVATION_MAIL_BODY = _("""
Hallo {}!

Bitte bestätige deine E-Mail-Adresse und aktiviere deinen Account bei deutschlandzusammen.de. Klicke dazu einfach
auf den folgenden Link oder kopiere ihn in die Adressleiste deines Browsers:

{}

Bis du deinen Account aktiviert hast können deine Angebote nicht gefunden werden.

Liebe Grüße
dein Team von deutschlandzusammen.de
""")

# Webpush

WEBPUSH_SETTINGS = {
    'VAPID_PUBLIC_KEY': 'BGLF2Ic8PYGm0syvEMoryf8z0tEvb5M3z0xgLiWuvdvG1oP7A_OXBcSGjPMycg__5Ex1xEGHy_CiQYwRniiJB-g',
    'VAPID_PRIVATE_KEY': 'ey-8QaP5B4nyMlbNpYKDw55TJ1AGfhMeXLbMMyMrISA',
    'VAPID_ADMIN_EMAIL': 'support@deutschlandzusammen.de'
}


# Prometheus

PROMETHEUS_PATH_SECRET = 'pass'


# Overview map

# radius is in degrees (lat/lng)
BLUR_RADIUS = 0.0075
