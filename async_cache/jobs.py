import time
import logging

from django.core.cache import cache

from async_cache import tasks

logger = logging.getLogger(__name__)

MEMCACHE_MAX_EXPIRATION = 2592000


class AsyncCacheJob(object):
    # Default cache lifetime is 5 minutes
    lifetime = 600
    # Default behaviour is to do a synchronous fetch when the cache is empty.
    # Stale results are generally ok, but not no results.
    fetch_on_empty = True

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
                logger.debug(("Job %s with key '%s' - cache MISS - running "
                              "synchronous refresh"),
                             self.class_path, key)
                return self.refresh(*args, **kwargs)
            else:
                logger.debug(("Job %s with key '%s' - cache MISS - triggering "
                              "async refresh and returning empty result"),
                             self.class_path, key)
                # Fetch empty result and put it in the cache as a dead result to
                # avoid cache hammering.
                empty = self.empty()
                self.cache_set(key, None, empty)
                self.async_refresh(key, *args, **kwargs)
                return empty

        if result[0] is None:
            # Cache is stale - but the cache refresh job has already been
            # triggered.  We return the stale result
            logger.debug(("Job %s with key '%s' - DEAD cache hit -  "
                          "refresh already triggered - returning stale result"),
                         self.class_path, key)
        elif result[0] < time.time():
            # Cache is stale - we trigger a refresh but allow the stale result
            # to be returned this time.  This is normally acceptable.
            logger.debug(("Job %s with key '%s' - STALE cache hit - triggering "
                          "async refresh and returning stale result"),
                         self.class_path, key)
            # We replace the item in the cache with one without a TTL - this
            # prevents cache hammering.
            self.cache_set(key, None, result[1])
            self.async_refresh(key, *args, **kwargs)
        else:
            logger.debug(("Job %s with key '%s' - cache HIT"), self.class_path,
                         key)
        return result[1]

    def cache_set(self, key, ttl, result):
        """
        Add a result to the cache
        """
        cache.set(key, (ttl, result), MEMCACHE_MAX_EXPIRATION)

    def refresh(self, *args, **kwargs):
        """
        Fetch the result SYNCHRONOUSLY and populate the cache
        """
        result = self.fetch(*args, **kwargs)
        self.cache_set(self.key(*args, **kwargs),
                       self.time_to_live(*args, **kwargs),
                       result)
        return result

    def async_refresh(self, key, *args, **kwargs):
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

    def time_to_live(self, *args, **kwargs):
        """
        Return the TTL for this item.
        """
        return time.time() + self.lifetime

    def key(self, *args, **kwargs):
        """
        Return the cache key to use.

        If no parameters are passed to the 'get' method then this method doesn
        not need to be overridden.
        """
        if not args and not kwargs:
            return self.class_path
        if args and not kwargs:
            return args
        return "%s-%s-%s" % (hash(args),
                             hash(tuple(kwargs.keys())),
                             hash(tuple(kwargs.values())))

    def fetch(self, *args, **kwargs):
        """
        Return the data for this job - this is where the expensive work should
        be encapsulated.
        """
        raise NotImplementedError()


class QuerySetJob(AsyncCacheJob):

    def __init__(self, model):
        self.model = model

    def key(self, *args, **kwargs):
        return "%s-%s" % (
            self.model.__name__,
            super(QuerySetJob, self).key(*args, **kwargs)
        )


class QuerySetGetJob(QuerySetJob):

    def fetch(self, *args, **kwargs):
        return self.model.objects.get(**kwargs)


class QuerySetFilterJob(QuerySetJob):

    def fetch(self, *args, **kwargs):
        return self.model.objects.filter(**kwargs)

