from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DeleteView, CreateView, UpdateView

from offers.forms import OfferSearchForm, UserForm, OfferForm, ProviderProfileForm
from offers.helper import location_from_address
from offers.models import Offer, ProviderProfile


class AccountRegistrationView(FormView):
    form_class = UserForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = AccountRegistrationView.register_user(self.request, **form.cleaned_data)
        login(self.request, user)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_active:
            return HttpResponseRedirect(reverse_lazy('profile'))
        else:
            return super().dispatch(request, *args, **kwargs)

    @classmethod
    def register_user(cls, request, **kwargs):
        user = User.objects.create_user(username=kwargs['username'], email=kwargs['email'], password=kwargs['password'],
                                 first_name=kwargs['first_name'], last_name=kwargs['last_name'])
        ProviderProfile.objects.create(user=user)
        return user


class EditProfileView(UpdateView):
    model = ProviderProfile
    form_class = ProviderProfileForm
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        return ProviderProfile.objects.filter(user=self.request.user)

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        self.request.user.first_name = form.cleaned_data['first_name']
        self.request.user.last_name = form.cleaned_data['last_name']
        self.request.user.save()
        return super().form_valid(form)


class ProfileView(ListView):
    model = Offer
    template_name = 'offers/providerprofile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.location is None:
            return HttpResponseRedirect(reverse_lazy('edit_profile', args=[request.user.profile.id]))
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Offer.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['mapbox_api_token'] = settings.MAPBOX_API_TOKEN
        return data


class DeleteOfferView(DeleteView):
    model = Offer
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        return Offer.objects.filter(user=self.request.user)


class CreateOfferView(CreateView):
    model = Offer
    form_class = OfferForm

    def get_success_url(self):
        return reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class OfferSearchView(FormView):
    form_class = OfferSearchForm
    template_name = 'offers/home.html'
    success_url = ''

    @staticmethod
    def get_queryset(form):
        location = location_from_address(form.cleaned_data['where'])
        time = form.cleaned_data['when']

        return Offer.offers_in_range_and_time(location, time)

    def form_valid(self, form):
        return render(self.request, 'offers/search_results.html', {
            'object_list': self.get_queryset(form),
        })
