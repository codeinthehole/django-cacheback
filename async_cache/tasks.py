import time

from django.core.cache import cache
from celery import task


class AsyncCacheJob(object):
    lifetime = 600 

    def get(self, *args, **kwargs):
        """
        Return the data for this function
        """
        key = self.key(*args, **kwargs)
        result = cache.get(key)
        now = time.time()
        if result is None:
            # Cache is empty - trigger a refresh and return the 'empty'
            # value
            self.refresh(key, *args, **kwargs)
            return self.empty()
        elif result[0] < now:
            # Cache is stale - we return the stale result but trigger a         
            # refresh.
            self.refresh(key, *args, **kwargs)
        return result[1]
    
    def refresh(self, key, *args, **kwargs):
        """
        Fetch the results and re-populate the cache
        """
        refresh_cache.delay(key, self.fetch, self.lifetime, *args, **kwargs)

    # Override these methods

    def empty(self):
        return None

    def key(self, *args, **kwargs):
        """
        Return the cache key to use
        """
        raise NotImplementedError()

    def fetch(self, *args, **kwargs):
        """
        Return the data for this job
        """
        raise NotImplementedError()


@task()
def refresh_cache(key, fn, ttl, *args, **kwargs):
    """
    Re-populate cache

    :key: Cache key
    :fn: Data fetching function
    :ttl: Time-to-live
    :args: Function args
    :kwargs: Function kwargs
    """
    results = fn(*args, **kwargs)
    cache.set(key, (ttl, results))