import time
import logging

from django.core.cache import cache

from async_cache import tasks

logger = logging.getLogger(__name__)

# We don't use memcache to handle expiry so all items are set using the max TTL.
MEMCACHE_MAX_EXPIRATION = 2592000


class AsyncCacheJob(object):
    """
    A cached read job
    """
    # All items are stored in memcache as a tuple (expiry, data).  We don't use the
    # TTL functionality within memcache but implement on own.  If the expiry value
    # is None, this indicates that there is already a job created for refreshing
    # this item.

    # Default cache lifetime is 5 minutes
    lifetime = 600

    # Default behaviour is to do a synchronous fetch when the cache is empty.
    # Stale results are generally ok, but not no results.
    fetch_on_empty = True

    def get(self, *args, **kwargs):
        """
        Return the data for this function (using the cache if possible).

        This method is not intended to be overidden
        """
        key = self.key(*args, **kwargs)
        result = cache.get(key)
        if result is None:
            # Cache is empty - we can either:
            # a) fetch the data immediately, blocking execution until
            #    the fetch has finished, or
            # b) trigger an async refresh and return an empty result
            if self.fetch_on_empty:
                logger.debug(("Job %s with key '%s' - cache MISS - running "
                              "synchronous refresh"),
                             self.class_path, key)
                return self.refresh(*args, **kwargs)
            else:
                logger.debug(("Job %s with key '%s' - cache MISS - triggering "
                              "async refresh and returning empty result"),
                             self.class_path, key)
                # Before triggering the async refersh, we fetch empty result and
                # put it in the cache as a dead result to avoid cache hammering.
                empty = self.empty()
                self.cache_set(key, None, empty)
                self.async_refresh(*args, **kwargs)
                return empty

        if result[0] is None:
            # Cache is dead - ie the cache refresh job has already been
            # triggered.  We return the stale result.
            logger.debug(("Job %s with key '%s' - DEAD cache hit -  "
                          "refresh already triggered - returning stale result"),
                         self.class_path, key)
        elif result[0] < time.time():
            # Cache is stale - we trigger a refresh but allow the stale result
            # to be returned this time.  This is normally acceptable.
            logger.debug(("Job %s with key '%s' - STALE cache hit - triggering "
                          "async refresh and returning stale result"),
                         self.class_path, key)
            # We replace the item in the cache with one without an expiry - this
            # prevents cache hammering.
            self.cache_set(key, None, result[1])
            self.async_refresh(*args, **kwargs)
        else:
            logger.debug(("Job %s with key '%s' - cache HIT"), self.class_path,
                         key)
        return result[1]

    def cache_set(self, key, expiry, data):
        """
        Add a result to the cache

        :key: Cache key to use
        :expiry: The expiry timestamp after which the result is stale
        :data: The data to cache
        """
        cache.set(key, (expiry, data), MEMCACHE_MAX_EXPIRATION)

    def refresh(self, *args, **kwargs):
        """
        Fetch the result SYNCHRONOUSLY and populate the cache
        """
        result = self.fetch(*args, **kwargs)
        self.cache_set(self.key(*args, **kwargs),
                       self.expiry(*args, **kwargs),
                       result)
        return result

    def async_refresh(self, *args, **kwargs):
        """
        Trigger an asynchronous job to refresh the cache
        """
        tasks.refresh_cache.delay(self.class_path, *args, **kwargs)

    @property
    def class_path(self):
        return '%s.%s' % (self.__module__, self.__class__.__name__)

    # Override these methods

    def empty(self):
        """
        Return the appropriate value for a cache MISS (and when we defer the
        repopulation of the cache)
        """
        return None

    def expiry(self, *args, **kwargs):
        """
        Return the expiry timestamp for this item.
        """
        return time.time() + self.lifetime

    def key(self, *args, **kwargs):
        """
        Return the cache key to use.

        If you're passing anything but primitive types to the ``get`` method,
        it's likely that you'll need to override this method.
        """
        if not args and not kwargs:
            return self.class_path
        try:
            if args and not kwargs:
                return hash(args)
            # The line might break if your passed values are un-hashable.  If it
            # does, you need to override this method and implement your own key
            # algorithm.
            return "%s:%s:%s" % (hash(args),
                                hash(tuple(kwargs.keys())),
                                hash(tuple(kwargs.values())))
        except TypeError:
            raise RuntimeError("Unable to generate cache key due to unhashable"
                               "args or kwargs - you need to implement your own"
                               "key generation method to avoid this problem")

    def fetch(self, *args, **kwargs):
        """
        Return the data for this job - this is where the expensive work should
        be done.
        """
        raise NotImplementedError()
