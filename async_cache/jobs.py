import time

from django.core.cache import cache

from async_cache import tasks


class AsyncCacheJob(object):
    lifetime = 600
    fetch_on_empty = False

    def get(self, *args, **kwargs):
        """
        Return the data for this function (using the cache if possible).
        """
        key = self.key(*args, **kwargs)
        result = cache.get(key)
        if result is None:
            # Cache is empty - we can either:
            # a) fetch the data immediately, blocking execution until
            #    the fetch has finished, or
            # b) trigger an async refresh
            if self.fetch_on_empty:
                return self.refresh(*args, **kwargs)
            else:
                self.async_refresh(key, *args, **kwargs)
                return self.empty()

        if result[0] < time.time():
            # Cache is stale - we trigger a refresh but allow the stale result
            # to be returned this time
            self.async_refresh(key, *args, **kwargs)
        return result[1]

    def refresh(self, *args, **kwargs):
        """
        Fetch the result SYNCHRONOUSLY and populate the cache
        """
        result = self.fetch(*args, **kwargs)
        cache.set(self.key(*args, **kwargs), (self.lifetime, result))
        return result

    def async_refresh(self, key, *args, **kwargs):
        """
        Fetch the results ASYNCHRONOUSLY and populate the cache
        """
        klass = '%s.%s' % (self.__module__, self.__class__.__name__)
        tasks.refresh_cache.delay(klass, *args, **kwargs)

    # Override these methods

    def empty(self):
        """
        Return the appropriate value for a cache miss (and when we defer the
        repopulation of the cache)
        """
        return None

    def key(self, *args, **kwargs):
        """
        Return the cache key to use
        """
        raise NotImplementedError()

    def fetch(self, *args, **kwargs):
        """
        Return the data for this job - this is where the expensive work should
        be encapsulated.
        """
        raise NotImplementedError()
