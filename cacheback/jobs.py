try:
    import importlib
except ImportError:
    import django.utils.importlib as importlib

from .base import Job


class FunctionJob(Job):
    """
    Job for executing a function and caching the result
    """

    def __init__(self, lifetime=None, fetch_on_miss=None, cache_alias=None,
                 task_options=None, set_data_kwarg=None):
        super(FunctionJob, self).__init__()
        if lifetime is not None:
            self.lifetime = int(lifetime)
        if fetch_on_miss is not None:
            self.fetch_on_miss = fetch_on_miss
        if cache_alias is not None:
            self.cache_alias = cache_alias
        if task_options is not None:
            self.task_options = task_options
        if set_data_kwarg is not None:
            self.set_data_kwarg = set_data_kwarg

    def get_init_kwargs(self):
        """
        Return the kwargs that need to be passed to __init__ when reconstructing
        this class.
        """
        # We don't need to pass fetch_on_miss as it isn't used by the refresh
        # method.
        return {'lifetime': self.lifetime,
                'cache_alias': self.cache_alias}

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


class QuerySetJob(Job):
    """
    Helper class for wrapping ORM reads
    """

    def __init__(self, model, lifetime=None, fetch_on_miss=None, cache_alias=None,
                 task_options=None):
        """
        :model: The model class to use
        """
        super(QuerySetJob, self).__init__()
        self.model = model
        if lifetime is not None:
            self.lifetime = lifetime
        if fetch_on_miss is not None:
            self.fetch_on_miss = fetch_on_miss
        if cache_alias is not None:
            self.cache_alias = cache_alias
        if task_options is not None:
            self.task_options = task_options

    def get_init_kwargs(self):
        return {'model': self.model,
                'lifetime': self.lifetime,
                'cache_alias': self.cache_alias}

    def key(self, *args, **kwargs):
        return "%s-%s" % (
            self.model.__name__,
            super(QuerySetJob, self).key(*args, **kwargs)
        )


class QuerySetGetJob(QuerySetJob):
    """
    For ORM reads that use the ``get`` method.
    """
    def fetch(self, *args, **kwargs):
        return self.model.objects.get(**kwargs)


class QuerySetFilterJob(QuerySetJob):
    """
    For ORM reads that use the ``filter`` method.
    """
    def fetch(self, *args, **kwargs):
        return self.model.objects.filter(**kwargs)
