from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DeleteView, CreateView, DetailView

from offers.forms import OfferSearchForm, UserForm
from offers.helper import location_from_address
from offers.models import Offer


class AccountRegistrationView(FormView):
    template_name = 'registration/registration.html'
    form_class = UserForm
    success_url = reverse_lazy('offers')

    def form_valid(self, form):
        AccountRegistrationView.register_user(self.request, **form.cleaned_data)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_active:
            return HttpResponseRedirect(reverse_lazy('offers'))
        else:
            return super().dispatch(request, *args, **kwargs)

    @classmethod
    def register_user(cls, request, **kwargs):
        User.objects.create_user(username=kwargs['username'], email=kwargs['email'], password=kwargs['password'],
                                 first_name=kwargs['first_name'], last_name=kwargs['last_name'])


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


class OffersListView(ListView):
    model = Offer

    def get_queryset(self):
        return Offer.objects.filter(user=self.request.user)


class DeleteOfferView(DeleteView):
    model = Offer
    success_url = reverse_lazy('offers')

    def get_queryset(self):
        return Offer.objects.filter(user=self.request.user)


class CreateOfferView(CreateView):
    model = Offer
    fields = ['title', 'radius', 'address', 'city', 'start_time', 'end_time', 'comment']

    def get_success_url(self):
        return reverse_lazy('offer_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.location = location_from_address('{}, {}'.format(form.instance.address, form.instance.city))
        return super().form_valid(form)


class OfferDetailView(DetailView):
    model = Offer

    def get_queryset(self):
        return Offer.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['mapbox_api_token'] = settings.MAPBOX_API_TOKEN
        return data
