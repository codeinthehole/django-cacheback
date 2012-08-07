from cacheback import AsyncCacheJob


class FunctionJob(AsyncCacheJob):

    def key(self, fn, *args, **kwargs):
        return '%s:%s:%s:%s:%s' % (
            fn.__module__, fn.__name__,
            hash(args), hash(tuple(kwargs.keys())),
            hash(tuple(kwargs.values())))

    def fetch(self, fn, *args, **kwargs):
        return fn(*args, **kwargs)
