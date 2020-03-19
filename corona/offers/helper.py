import json
import random
import string

import requests
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


def address_autocomplete(query):
    api_url = "http://photon.komoot.de/api/?q={}".format(query)

    response = requests.get(api_url)

    if response.status_code == 200:
        data = json.loads(response.content.decode('UTF-8'))
        suggestions = set(["{}, {}".format(result['properties']['name'],
                                           result['properties']['city'] if 'city' in result['properties'] else "")
                           for result in data['features']
                           if 'country' in result['properties'] and result['properties']['country'] == 'Germany'])
        return list(suggestions)
    else:
        return [query]


def create_activation_token():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(64))


def create_profile_slug():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(20))
