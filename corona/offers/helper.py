import json

from django.conf import settings
from django.contrib.gis.geos import Point
from geopy import Nominatim
from geopy.exc import GeocoderQueryError

DEFAULT_POINT = Point(49.877212, 8.655164, srid=settings.SRID)


def location_from_address(address):
    locator = Nominatim(user_agent=settings.NOMINATIM_USER_AGENT)

    try:
        location = locator.geocode(address)
    except GeocoderQueryError:
        return DEFAULT_POINT

    if location:
        return Point(location.latitude, location.longitude, srid=settings.SRID)
    else:
        return DEFAULT_POINT


def address_from_location(lat, lng):
    locator = Nominatim(user_agent=settings.NOMINATIM_USER_AGENT)

    try:
        location = locator.reverse("{}, {}".format(lat, lng))
    except GeocoderQueryError:
        return ""

    return location.raw['display_name'] if location else ""
