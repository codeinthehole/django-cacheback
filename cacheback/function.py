from django.utils import importlib

from cacheback import AsyncCacheJob


class FunctionJob(AsyncCacheJob):
    """
    Job for executing a function and caching the result
    """

    def __init__(self, lifetime=None, fetch_on_miss=None):
        if lifetime is not None:
            self.lifetime = int(lifetime)
        if fetch_on_miss is not None:
            self.fetch_on_miss = fetch_on_miss

    def prepare_args(self, fn, *args):
        # Convert function into "module:name" form so that is can be pickled and
        # then re-imported.
        return ("%s:%s" % (fn.__module__, fn.__name__),) + args

    def fetch(self, fn_string, *args, **kwargs):
        # Import function from string representation
        module_path, fn_name = fn_string.split(":")
        module = importlib.import_module(module_path)
        fn = getattr(module, fn_name)
        # Look for a raw function attribute - this is set by the decorator.
        if hasattr(fn, 'fn'):
            fn = fn.fn
        return fn(*args, **kwargs)

    def get_constructor_kwargs(self):
        """
        Return the kwargs that need to be passed to __init__ when reconstructing
        this class.
        """
        return {'lifetime': self.lifetime,
                'fetch_on_miss': self.fetch_on_miss}


def cacheback(lifetime=None):
    job = FunctionJob()
    def wrapper(fn):
        def _wrapper(*args, **kwargs):
            # Assign reference to unwrapped function so that we can access it
            # later without incurring infinite regress.
            _wrapper.fn = fn
            return job.get(fn, lifetime, *args, **kwargs)
        return _wrapper
    return wrapper
