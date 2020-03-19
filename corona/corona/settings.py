"""
Django settings for corona project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tm4nzh33&pt64sp_wsmir02w7j1da=jf+6f$i2xpnn+m8or948'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', 'deutschlandzusammen.de', 'www.deutschlandzusammen.de']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'bootstrap4',
    'captcha',
    'offers',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
        'NAME': 'gis' if DEBUG else 'koronadb',
        'USER': 'gis' if DEBUG else 'koronadb',
        'PASSWORD': 'changeme1' if DEBUG else '2vU8DyFpTedf54Z3Dkb3',
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

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

if not DEBUG:
    STATIC_ROOT = '/var/www/virtual/korona/html/static'


# Geography settings

SRID = 4326
NOMINATIM_USER_AGENT = "corona-hilfsangebote"

MAPBOX_API_TOKEN = "pk.eyJ1IjoiamxhdWluZ2VyIiwiYSI6ImNrN3RzMWcyNjB3Z3IzbXFyZmZianRkZzAifQ.P0LQjvZ7G0dB9uNqs2r3YQ"

if not DEBUG:
    GDAL_LIBRARY_PATH = '/home/korona/lib/libgdal.so'
    GEOS_LIBRARY_PATH = '/home/korona/lib/libgeos_c.so'


# Auth settings

LOGIN_REDIRECT_URL = '/profile'
LOGOUT_REDIRECT_URL = '/'


# Contact mail settings

EMAIL_HOST = "localhost"
EMAIL_PORT = 1025 if DEBUG else 587

if not DEBUG:
    EMAIL_USE_TLS = True

    EMAIL_HOST_USER = 'noreply@deutschlandzusammen.de'
    EMAIL_HOST_PASSWORD = 'FoqNEeX5YW9MmDizdQi6'

    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    SERVER_EMAIL = EMAIL_HOST_USER

CONTACT_MAIL_FROM = 'noreply@deutschlandzusammen.de'
CONTACT_MAIL_SUBJECT = 'Neue Nachricht von Corona-Hilfsangebote'
CONTACT_MAIL_BODY = """Hallo {}!

Du hast eine neue Anfrage nach Hilfe über deutschlandzusammen.de!

Daten zur suchenden Person:
Name: {}
E-Mail: {}
Telefon: {}
Geschlecht: {}

Nachricht:
{}

Melde dich doch wenn du kannst schnellstmöglich zurück.

Liebe Grüße
dein Team von deutschlandzusammen.de
"""

HOST_NAME = 'http://localhost:8000' if DEBUG else 'https://www.deutschlandzusammen.de'
ACTIVATION_MAIL_FROM = 'noreply@deutschlandzusammen.de'
ACTIVATION_MAIL_SUBJECT = 'Aktiviere deinen Account bei deutschlandzusammen.de'
ACTIVATION_MAIL_BODY = """
Hallo {}!

Bitte bestätige deine E-Mail-Adresse und aktiviere deinen Account bei deutschlandzusammen.de. Klicke dazu einfach
auf den folgenden Link oder kopiere ihn in die Adressleiste deines Browsers:

{}

Bis du deinen Account aktiviert hast können deine Angebote nicht gefunden werden.

Liebe Grüße
dein Team von deutschlandzusammen.de
"""