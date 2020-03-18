import json
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views import View
from django.views.generic import FormView, ListView, UpdateView, TemplateView, DeleteView

from offers.forms import OfferSearchForm, UserForm, ProviderProfileForm, SendMessageForm, OfferFormSet
from offers.helper import location_from_address, address_from_location, address_autocomplete
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
        user = User.objects.create_user(username=kwargs['username'], email=kwargs['email'], password=kwargs['password'])
        ProviderProfile.objects.create(user=user)
        return user


class DeleteUserView(DeleteView):
    model = User
    success_url = reverse_lazy('search')
    template_name = 'registration/user_confirm_delete.html'

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class ProfileView(ListView):
    model = Offer
    template_name = 'offers/providerprofile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.location is None:
            return HttpResponseRedirect(reverse_lazy('edit_profile', args=[request.user.profile.id]))
        elif self.user_has_no_active_times():
            return HttpResponseRedirect(reverse_lazy('offers'))
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Offer.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['mapbox_api_token'] = settings.MAPBOX_API_TOKEN
        return data

    def user_has_no_active_times(self):
        return not Offer.objects.filter(user=self.request.user).exists()


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


class OffersView(FormView):
    template_name = 'offers/offers_list.html'

    def get_queryset(self):
        return Offer.objects.filter(user=self.request.user)

    def get_form(self, form_class=None):
        return OfferFormSet(queryset=self.get_queryset(), **self.get_form_kwargs())

    def get_initial(self):
        dates = [now() + timedelta(days=n) for n in range(14)]
        return [{'date': date.date()} for date in dates if not self.get_queryset().filter(date=date).exists()]

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['any_offers_exist'] = self.any_offer_exists()
        return context_data

    def get_success_url(self):
        return reverse_lazy('profile') if self.any_offer_exists() else reverse_lazy('offers')

    def form_valid(self, form):
        for form in form:
            if self.contains_any_active_time(form):
                form.instance.user = self.request.user
                form.save()
            elif form.cleaned_data['id'] and form.instance.user == self.request.user:
                form.instance.delete()

        return super().form_valid(form)

    @staticmethod
    def contains_any_active_time(form):
        return form.cleaned_data['morning'] or form.cleaned_data['noon'] or \
               form.cleaned_data['afternoon'] or form.cleaned_data['evening']

    def any_offer_exists(self):
        return self.get_queryset().exists()


class OfferSearchView(FormView):
    form_class = OfferSearchForm
    template_name = 'offers/home.html'
    success_url = ''

    @staticmethod
    def get_location_and_objects(form):
        location = location_from_address(form.cleaned_data['where'])
        date = form.cleaned_data['when']

        return location, Offer.offers_in_range_and_date(location, date)

    def get_initial(self):
        initial = super().get_initial()
        initial['when'] = now().__format__('%d.%m.%Y')
        return initial

    def form_valid(self, form):
        location, objects = self.get_location_and_objects(form)

        return render(self.request, 'offers/search_results.html', {
            'location': location,
            'object_list': objects,
            'mapbox_api_token': settings.MAPBOX_API_TOKEN
        })


class SendMessageView(UpdateView):
    model = User
    form_class = SendMessageForm
    template_name = 'offers/send_message.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['gender'] = 'X'
        return initial

    def form_valid(self, form):
        SendMessageView.send_message(form.instance, form.cleaned_data['sender'], form.cleaned_data['email'],
                                     form.cleaned_data['phone'], form.cleaned_data['gender'],
                                     form.cleaned_data['message'])
        return HttpResponseRedirect(reverse_lazy('message_sent'))

    @staticmethod
    def send_message(user, sender, sender_email, sender_phone, sender_gender, message):
        body = """
        Hallo {}!
        
        Du hast eine neue Anfrage nach Hilfe über deutschlandzusammen.de!
        
        Daten zur suchenden Person:
        Name: {}
        E-Mail: {}
        Telefon: {}
        Geschlecht: {}
        
        Nachricht:
        {}
        
        ---
        
        Melde dich doch wenn du kannst schnellstmöglich zurück.
        
        Liebe Grüße
        dein Team von deutschlandzusammen.de
        """.format(user.first_name, sender, sender_email, sender_phone, sender_gender, message)
        send_mail(settings.CONTACT_MAIL_SUBJECT, body, settings.CONTACT_MAIL_FROM, [user.email], fail_silently=True)


class MessageSentView(TemplateView):
    template_name = 'offers/message_sent.html'


class SafetyInformationView(TemplateView):
    template_name = 'offers/safety_information.html'


class AddressFromLocationAjaxView(View):
    def get(self, request):
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')

        return HttpResponse(address_from_location(lat, lng))


class AddressAutocompleteAjaxView(View):
    def get(self, request):
        query = request.GET.get('q')

        return HttpResponse(json.dumps(address_autocomplete(query)))
