import warnings

from .apps import CachebackConfig  # noqa
from .utils import RemovedInCacheback13Warning


warnings.warn(
    '`cacheback.conf.CachebackConfig` is deprecated, '
    'use `cacheback.apps.CachebackConfig` instead.',
    RemovedInCacheback13Warning
)
