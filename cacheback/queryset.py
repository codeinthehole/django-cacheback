import warnings

from .jobs import QuerySetFilterJob, QuerySetGetJob, QuerySetJob  # noqa
from .utils import RemovedInCacheback13Warning


warnings.warn(
    '`cacheback.queryset` is deprecated, use `cacheback.jobs` instead.',
    RemovedInCacheback13Warning
)
