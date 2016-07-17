import warnings

from .jobs import FunctionJob  # noqa
from .utils import RemovedInCacheback13Warning


warnings.warn(
    '`cacheback.function` is deprecated, use `cacheback.jobs` instead.',
    RemovedInCacheback13Warning
)
