from django.contrib.auth.decorators import login_required
from django.urls import path

from offers.views import OfferSearchView, ProfileView, DeleteOfferView, CreateOfferView, EditProfileView

urlpatterns = [
    path('offers/new/', login_required(CreateOfferView.as_view()), name='create_offer'),
    path('offers/<int:pk>/delete/', login_required(DeleteOfferView.as_view()), name='delete_offer'),
path('profile/', login_required(ProfileView.as_view()), name='profile'),
    path('profile/<int:pk>/edit/', login_required(EditProfileView.as_view()), name='edit_profile'),
    path('', OfferSearchView.as_view(), name='search'),
]


