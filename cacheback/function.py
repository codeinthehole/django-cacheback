from .jobs import FunctionJob  # noqa
from .utils import warn_deprecation


warn_deprecation(
    '`cacheback.function` is deprecated, use `cacheback.jobs` instead.')
