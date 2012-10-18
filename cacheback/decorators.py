from functools import wraps
from django.utils.decorators import available_attrs

from cacheback.function import FunctionJob

def cacheback(lifetime=None, fetch_on_miss=None, job_class=None):
    """
    Decorate function to cache its return value using the CacheBack job class.

    :lifetime: How long to cache items for
    :fetch_on_miss: Whether to perform a synchronous
    """
    if job_class is None:
        job_class = FunctionJob
    job = job_class(lifetime, fetch_on_miss)

    def _wrapper(fn):
        # using available_attrs to work around http://bugs.python.org/issue3445
        @wraps(fn, assigned=available_attrs(fn))
        def __wrapper(*args, **kwargs):
            return job.get(fn, *args, **kwargs)
        # Assign reference to unwrapped function so that we can access it
        # later without descending into infinite regress.
        __wrapper.fn = fn
        return __wrapper

    return _wrapper
