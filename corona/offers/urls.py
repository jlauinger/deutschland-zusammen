from django.contrib.auth.decorators import login_required
from django.urls import path

from offers.views import OfferSearchView, OffersListView, DeleteOfferView, CreateOfferView, OfferDetailView

urlpatterns = [
    path('offers/', login_required(OffersListView.as_view()), name='offers'),
    path('offers/new/', login_required(CreateOfferView.as_view()), name='create_offer'),
    path('offers/<int:pk>/delete/', login_required(DeleteOfferView.as_view()), name='delete_offer'),
    path('offers/<int:pk>/', login_required(OfferDetailView.as_view()), name='offer_detail'),
    path('', OfferSearchView.as_view(), name='search'),
]

