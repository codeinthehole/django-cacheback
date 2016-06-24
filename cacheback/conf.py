from .apps import CachebackConfig  # noqa
from .utils import warn_deprecation


warn_deprecation(
    '`cacheback.conf.CachebackConfig` is deprecated, '
    'use `cacheback.apps.CachebackConfig` instead.'
)
