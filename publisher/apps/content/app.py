from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ContentAppConfig(AppConfig):
    name = 'publisher.apps.content'
    verbose_name = _('content')
