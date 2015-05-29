try:
    import importlib
except ImportError:
    import django.utils.importlib as importlib

from cacheback.base import Job


class FunctionJob(Job):
    """
    Job for executing a function and caching the result
    """

    def __init__(self, lifetime=None, fetch_on_miss=None, task_options=None):
        super(FunctionJob, self).__init__()
        if lifetime is not None:
            self.lifetime = int(lifetime)
        if fetch_on_miss is not None:
            self.fetch_on_miss = fetch_on_miss
        if task_options is not None:
            self.task_options = task_options

    def prepare_args(self, fn, *args):
        # Convert function into "module:name" form so that is can be pickled and
        # then re-imported.
        return ("%s:%s" % (fn.__module__, fn.__name__),) + args

    def fetch(self, fn_string, *args, **kwargs):
        # Import function from string representation
        module_path, fn_name = fn_string.split(":")
        module = importlib.import_module(module_path)
        fn = getattr(module, fn_name)
        # Look for 'fn' attribute which is used by the decorator
        if hasattr(fn, 'fn'):
            fn = fn.fn
        return fn(*args, **kwargs)

    def get_constructor_kwargs(self):
        """
        Return the kwargs that need to be passed to __init__ when reconstructing
        this class.
        """
        # We don't need to pass fetch_on_miss as it isn't used by the refresh
        # method.
        return {'lifetime': self.lifetime}
