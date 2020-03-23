from django.contrib.auth.decorators import login_required
from django.urls import path

from offers.views import OfferSearchView, ProfileView, EditProfileView, \
    SendMessageView, MessageSentView, SafetyInformationView, AddressFromLocationAjaxView, AddressAutocompleteAjaxView, \
    OffersView, DeleteUserView, MessageErrorView, ActivateAccountView, ResendActivationMailView, MessagesView, \
    PushNotificationServiceWorkerView, ImprintView, PrivacyDeclarationView, ChangePasswordView, OverviewMapView

urlpatterns = [
    path('offers/', login_required(OffersView.as_view()), name='offers'),
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
    path('profile/change_password/', login_required(ChangePasswordView.as_view()), name='change_password'),
    path('profile/<str:slug>/edit/', login_required(EditProfileView.as_view()), name='edit_profile'),
    path('profile/<int:pk>/delete/', login_required(DeleteUserView.as_view()), name='delete_user'),
    path('profile/<str:slug>/message/', SendMessageView.as_view(), name='send_message'),
    path('map/', OverviewMapView.as_view(), name='overview_map'),
    path('messages/', login_required(MessagesView.as_view()), name='messages'),
    path('message/sent/', MessageSentView.as_view(), name='message_sent'),
    path('message/error/', MessageErrorView.as_view(), name='message_error'),
    path('information/safety/', SafetyInformationView.as_view(), name='safety_information'),
    path('ajax/address/', AddressFromLocationAjaxView.as_view(), name='ajax_address'),
    path('ajax/autocomplete/', AddressAutocompleteAjaxView.as_view(), name='ajax_autocomplete'),
    path('activate/resend-mail/', login_required(ResendActivationMailView.as_view()), name='resend_activation_mail'),
    path('activate/<str:slug>/<str:token>/', ActivateAccountView.as_view(), name='activate_account'),
    path('imprint/', ImprintView.as_view(), name='imprint'),
    path('privacy/', PrivacyDeclarationView.as_view(), name='privacy'),
    path('sw.js', PushNotificationServiceWorkerView.as_view(), name='push_service_worker'),
    path('', OfferSearchView.as_view(), name='search'),
]


