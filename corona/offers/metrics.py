from prometheus_client import Gauge

from offers.models import ProviderProfile, Message, Offer

Gauge('app_model_count_profile', 'Number of profiles currently existing').set(ProviderProfile.objects.count())
Gauge('app_model_count_offer', 'Number of offers currently existing').set(Offer.objects.count())
Gauge('app_model_count_message', 'Number of messages currently existing').set(Message.objects.count())
