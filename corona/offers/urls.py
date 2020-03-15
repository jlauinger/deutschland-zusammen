from django.contrib.auth.decorators import login_required
from django.urls import path

from offers.views import OfferSearchView, OffersListView, DeleteOfferView

urlpatterns = [
    path('offers/', login_required(OffersListView.as_view()), name='offers'),
    path('offers/<int:pk>/delete', login_required(DeleteOfferView.as_view()), name='delete_offer'),
    path('', OfferSearchView.as_view(), name='search'),
]
