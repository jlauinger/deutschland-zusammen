from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import FormView, ListView

from offers.forms import OfferSearchForm
from offers.helper import location_from_address
from offers.models import Offer


class OfferSearchView(FormView):
    form_class = OfferSearchForm
    template_name = 'home.html'
    success_url = ''

    @staticmethod
    def get_queryset(form):
        location = location_from_address(form.cleaned_data['where'])
        time = form.cleaned_data['when']

        return Offer.offers_in_range_and_time(location, time)

    def form_valid(self, form):
        return render(self.request, 'search_results.html', {
            'object_list': self.get_queryset(form),
        })


@login_required
class OffersListView(ListView):
    model = Offer


