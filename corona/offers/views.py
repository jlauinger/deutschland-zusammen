import json
from datetime import timedelta
from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import FormView, ListView, UpdateView, TemplateView, DeleteView

from offers.forms import OfferSearchForm, UserForm, ProviderProfileForm, SendMessageForm, OfferFormSet
from offers.helper import location_from_address, address_from_location, address_autocomplete
from offers.mail_templates import CONTACT_MAIL_BODY
from offers.models import Offer, ProviderProfile, Message
from offers.metrics import DUMMY


class AccountRegistrationView(FormView):
    form_class = UserForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('profile')
    metrics_import_dummy = DUMMY

    def form_valid(self, form):
        user = self.register_user(self.request, **form.cleaned_data)
        login(self.request, user)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_active:
            return HttpResponseRedirect(reverse_lazy('profile'))
        else:
            return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def register_user(request, **kwargs):
        user = User.objects.create_user(username=kwargs['username'], email=kwargs['email'], password=kwargs['password'])
        profile = ProviderProfile.objects.create(user=user)
        profile.send_activation_mail()
        return user


class ActivateAccountView(View):
    def get(self, request, **kwargs):
        success = self.activate_account(**kwargs)
        if success:
            messages.add_message(request, messages.SUCCESS, _('Dein Account wurde aktiviert!'))
            return HttpResponseRedirect(reverse_lazy('profile'))
        else:
            return render(self.request, 'registration/account_activation_failure.html')

    def activate_account(self, **kwargs):
        queryset = ProviderProfile.objects.filter(slug=kwargs['slug'], activation_token=kwargs['token'])

        if not queryset.exists():
            logout(self.request)
            return False

        profile = queryset[0]
        profile.activated = True
        profile.save()

        login(self.request, profile.user)

        return True


class ResendActivationMailView(View):
    def get(self, request):
        profile = ProviderProfile.objects.filter(user=request.user).first()
        profile.send_activation_mail()
        messages.add_message(request, messages.SUCCESS, _('Wir haben dir die Aktivierungs-Mail erneut gesendet!'))
        return HttpResponseRedirect(reverse_lazy('profile'))


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
            return HttpResponseRedirect(reverse_lazy('edit_profile', args=[request.user.profile.slug]))
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
        initial['email'] = self.request.user.email
        return initial


class ChangePasswordView(PasswordChangeView):
    success_url = reverse_lazy('profile')


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


class MessagesView(ListView):
    model = Message
    template_name = 'offers/messages.html'

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user).order_by('-date')


class OfferSearchView(FormView):
    form_class = OfferSearchForm
    template_name = 'offers/home.html'
    success_url = ''

    @staticmethod
    def get_location_and_objects(form):
        location = location_from_address(form.cleaned_data['where'])
        date = form.cleaned_data['when']
        mobility = form.cleaned_data['mobility']
        daytime = form.cleaned_data['daytime']

        print(mobility)
        print(daytime)

        offers = Offer.offers_in_range_and_date(location, date)

        if mobility != '' and mobility != 'NA':
            offers = offers.filter(user__profile__mobility=mobility)

        if daytime == 'MORNING':
            offers = offers.filter(morning=True)
        elif daytime == 'NOON':
            offers = offers.filter(noon=True)
        elif daytime == 'AFTERNOON':
            offers = offers.filter(afternoon=True)
        elif daytime == 'EVENING':
            offers = offers.filter(evening=True)

        return location, offers

    @staticmethod
    def is_filter_active(form):
        return form.cleaned_data['mobility'] or form.cleaned_data['daytime']

    def get_initial(self):
        initial = super().get_initial()
        initial['when'] = now().__format__('%d.%m.%Y')
        return initial

    def form_valid(self, form):
        location, objects = self.get_location_and_objects(form)

        return render(self.request, 'offers/search_results.html', {
            'form': form,
            'filter_active': self.is_filter_active(form),
            'location': location,
            'object_list': objects,
            'mapbox_api_token': settings.MAPBOX_API_TOKEN
        })


class OverviewMapView(ListView):
    model = ProviderProfile
    template_name = 'offers/overview_map.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mapbox_api_token'] = settings.MAPBOX_API_TOKEN
        context_data['initial_zoom'] = settings.OVERVIEW_MAP_INITIAL_ZOOM
        return context_data


class SendMessageView(UpdateView):
    model = ProviderProfile
    form_class = SendMessageForm
    template_name = 'offers/send_message.html'

    def form_valid(self, form):
        body = _(CONTACT_MAIL_BODY).format(name=form.instance.display_name,
                                                    sender_name=form.cleaned_data['sender'],
                                                    sender_email=form.cleaned_data['email'],
                                                    sender_phone=form.cleaned_data['phone'],
                                                    message=form.cleaned_data['message'],
                                                    domain=settings.DOMAIN_TEXT)

        message = Message.objects.create(recipient=form.instance.user, sender_name=form.cleaned_data['sender'],
                                         sender_email=form.cleaned_data['email'],
                                         sender_phone=form.cleaned_data['phone'],
                                         message=body,
                                         date=now())

        try:
            message.send()
        except SMTPException:
            return HttpResponseRedirect(reverse_lazy('message_error'))

        return HttpResponseRedirect(reverse_lazy('message_sent'))


class MessageSentView(TemplateView):
    template_name = 'offers/message_sent.html'


class MessageErrorView(TemplateView):
    template_name = 'offers/message_error.html'


class SafetyInformationView(TemplateView):
    template_name = 'offers/safety_information.html'


class PushNotificationServiceWorkerView(TemplateView):
    template_name = 'offers/sw.js'
    content_type = 'application/x-javascript'


class CssView(TemplateView):
    template_name = 'offers/styles.css'
    content_type = 'text/css'


class ImprintView(TemplateView):
    template_name = 'offers/imprint.html'


class PrivacyDeclarationView(TemplateView):
    template_name = 'offers/privacy.html'


class AddressFromLocationAjaxView(View):
    def get(self, request):
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')

        return HttpResponse(address_from_location(lat, lng))


class AddressAutocompleteAjaxView(View):
    def get(self, request):
        query = request.GET.get('q')

        return HttpResponse(json.dumps(address_autocomplete(query)))
