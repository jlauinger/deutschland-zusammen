from prometheus_client import Gauge

from offers.models import ProviderProfile, Message, Offer


DUMMY = 'unused value so that the import of the metrics file is not optimized'

Gauge('app_model_count_profile', 'Number of profiles currently existing').set(ProviderProfile.objects.count())
Gauge('app_model_count_offer', 'Number of offers currently existing').set(Offer.objects.count())
Gauge('app_model_count_message', 'Number of messages currently existing').set(Message.objects.count())
