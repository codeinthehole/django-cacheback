from functools import wraps

from django.utils.decorators import available_attrs

from .jobs import FunctionJob


def cacheback(lifetime=None, fetch_on_miss=None, cache_alias=None,
              job_class=None, task_options=None, **job_class_kwargs):
    """
    Decorate function to cache its return value.

    :lifetime: How long to cache items for
    :fetch_on_miss: Whether to perform a synchronous fetch when no cached
                    result is found
    :cache_alias: The Django cache alias to store the result into.
    :job_class: The class to use for running the cache refresh job.  Defaults
                using the FunctionJob.
    :job_class_kwargs: Any extra kwargs to pass to job_class constructor.
                       Useful with custom job_class implementations.
    """
    if job_class is None:
        job_class = FunctionJob
    job = job_class(lifetime=lifetime, fetch_on_miss=fetch_on_miss,
                    cache_alias=cache_alias, task_options=task_options,
                    **job_class_kwargs)

    def _wrapper(fn):
        # using available_attrs to work around http://bugs.python.org/issue3445
        @wraps(fn, assigned=available_attrs(fn))
        def __wrapper(*args, **kwargs):
            return job.get(fn, *args, **kwargs)
        # Assign reference to unwrapped function so that we can access it
        # later without descending into infinite regress.
        __wrapper.fn = fn
        # Assign reference to job so we can use the full Job API
        __wrapper.job = job
        return __wrapper

    return _wrapper
