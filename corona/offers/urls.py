from django.contrib.auth.decorators import login_required
from django.urls import path

from offers.views import OfferSearchView, ProfileView, DeleteOfferView, CreateOfferView, EditProfileView, \
    SendMessageView, MessageSentView, SafetyInformationView, AddressFromLocationAjaxView, AddressAutocompleteAjaxView

urlpatterns = [
    path('offers/new/', login_required(CreateOfferView.as_view()), name='create_offer'),
    path('offers/<int:pk>/delete/', login_required(DeleteOfferView.as_view()), name='delete_offer'),
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
    path('profile/<int:pk>/edit/', login_required(EditProfileView.as_view()), name='edit_profile'),
    path('profile/<int:pk>/message/', SendMessageView.as_view(), name='send_message'),
    path('sent/', MessageSentView.as_view(), name='message_sent'),
    path('information/safety/', SafetyInformationView.as_view(), name='safety_information'),
    path('ajax/address/', AddressFromLocationAjaxView.as_view(), name='ajax_address'),
    path('ajax/autocomplete/', AddressAutocompleteAjaxView.as_view(), name='ajax_autocomplete'),
    path('', OfferSearchView.as_view(), name='search'),
]


