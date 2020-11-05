from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CachebackConfig(AppConfig):
    name = 'cacheback'
    verbose_name = _('Cacheback')
