from django.urls import path

from offers.views import OfferSearchView


urlpatterns = [
    path('', OfferSearchView.as_view(), name='search'),
]
