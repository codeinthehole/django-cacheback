from .jobs import QuerySetFilterJob, QuerySetGetJob, QuerySetJob  # noqa
from .utils import warn_deprecation


warn_deprecation(
    '`cacheback.queryset` is deprecated, use `cacheback.jobs` instead.')
