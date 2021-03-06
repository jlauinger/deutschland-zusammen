from django.conf import settings


def vapid_key(request):
    return {
        'vapid_key': settings.WEBPUSH_SETTINGS.get('VAPID_PUBLIC_KEY')
    }


def multi_site(request):
    return {
        'hostname': settings.HOST_NAME,
        'domain_text': settings.DOMAIN_TEXT,
        'logo_url': settings.LOGO,
        'slideshow_first_image': settings.SLIDESHOW_FIRST_IMAGE,
        'default_point_lat': settings.DEFAULT_POINT_LAT,
        'default_point_lng': settings.DEFAULT_POINT_LNG,
    }
