from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DeleteView, CreateView

from offers.forms import OfferSearchForm
from offers.helper import location_from_address
from offers.models import Offer


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


class CreateOfferView(CreateView):
    model = Offer
    fields = ['title', 'radius', 'address', 'city', 'start_time', 'end_time', 'comment']
    success_url = reverse_lazy('offers')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.location = location_from_address('{}, {}'.format(form.instance.address, form.instance.city))
        return super().form_valid(form)
