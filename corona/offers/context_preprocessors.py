from django.conf import settings


def vapid_key(request):
    return {
        'vapid_key': settings.WEBPUSH_SETTINGS.get('VAPID_PUBLIC_KEY')
    }


def hostname(request):
    return {
        'hostname': settings.HOST_NAME,
        'domain_text': settings.DOMAIN_TEXT,
        'logo_url': settings.LOGO
    }
