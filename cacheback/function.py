from cacheback import AsyncCacheJob
from django.utils import importlib


class FunctionJob(AsyncCacheJob):

    def prepare_args(self, args):
        # Convert function into module:name form
        fn = args[0]
        return ("%s:%s" % (fn.__module__, fn.__name__),) + args[1:]

    def fetch(self, fn_string, *args, **kwargs):
        # Import function from string representation
        module_path, fn_name = fn_string.split(":")
        module = importlib.import_module(module_path)
        fn = getattr(module, fn_name)
        if hasattr(fn, 'fn'):
            fn = fn.fn
        return fn(*args, **kwargs)


def cacheback(lifetime=None):
    job = FunctionJob()
    if lifetime:
        job.lifetime = lifetime
    def wrapper(fn):
        def _wrapper(*args, **kwargs):
            # Assign reference to unwrapped function so that we can access it
            # later without incurring infinite regress.
            _wrapper.fn = fn
            return job.get(fn, *args, **kwargs)
        return _wrapper
    return wrapper
