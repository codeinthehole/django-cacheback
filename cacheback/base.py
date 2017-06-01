import collections
import hashlib
import logging
import time
import warnings

from django.conf import settings
from django.core.cache import DEFAULT_CACHE_ALIAS, caches
from django.db.models import Model as DjangoModel
from django.utils import six
from django.utils.deprecation import RenameMethodsBase
from django.utils.itercompat import is_iterable

from .utils import RemovedInCacheback13Warning, enqueue_task, get_job_class


logger = logging.getLogger('cacheback')

MEMCACHE_MAX_EXPIRATION = 2592000


# Container for call args (which makes things simpler to pass around)
Call = collections.namedtuple("Call", ['args', 'kwargs'])


def to_bytestring(value):
    """
    Encode an object as a UTF8 bytestring.  This function could be passed a
    bytestring, unicode string or object so must distinguish between them.

    :param value: object we want to transform into a bytestring
    :returns: a bytestring
    """
    if isinstance(value, DjangoModel):
        return ('%s:%s' % (value.__class__, hash(value))).encode('utf-8')
    if isinstance(value, six.text_type):
        return value.encode('utf8')
    if isinstance(value, six.binary_type):
        return value
    if six.PY2:
        return str(value)
    return bytes(str(value), 'utf8')


class JobBase(RenameMethodsBase):

    renamed_methods = (
        ('get_constructor_args', 'get_init_args', RemovedInCacheback13Warning),
        ('get_constructor_kwargs', 'get_init_kwargs', RemovedInCacheback13Warning),
        ('cache_set', 'store', RemovedInCacheback13Warning),
    )


class Job(six.with_metaclass(JobBase)):
    """
    A cached read job.

    This is the core class for the package which is intended to be subclassed
    to allow the caching behaviour to be customised.
    """
    # All items are stored in memcache as a tuple (expiry, data).  We don't use
    # the TTL functionality within memcache but implement on own.  If the
    # expiry value is None, this indicates that there is already a job created
    # for refreshing this item.

    #: Default cache lifetime is 10 minutes.  After this time, the result will
    #: be considered stale and requests will trigger a job to refresh it.
    lifetime = 600

    #: Timeout period during which no new tasks will be created for a
    #: single cache item.  This time should cover the normal time required to
    #: refresh the cache.
    refresh_timeout = 60

    #: Secifies which cache to use from your `CACHES` setting. It defaults to
    #: `default`.
    cache_alias = None

    #: Time to store items in the cache.  After this time, we will get a cache
    #: miss which can lead to synchronous refreshes if you have
    #: fetch_on_miss=True.
    cache_ttl = MEMCACHE_MAX_EXPIRATION

    #: Whether to perform a synchronous refresh when a result is missing from
    #: the cache.  Default behaviour is to do a synchronous fetch when the cache is empty.
    #: Stale results are generally ok, but not no results.
    fetch_on_miss = True

    #: Whether to perform a synchronous refresh when a result is in the cache
    #: but stale from. Default behaviour is never to do a synchronous fetch but
    #: there will be times when an item is _too_ stale to be returned.
    fetch_on_stale_threshold = None

    #: parameter name to pass in the data which is to be cached in the set method. Data can
    #: also be passed as last positional argument in set method, but using a kw arg may be
    #: clearer or even necessary. Defaults to 'data'
    set_data_kwarg = 'data'

    #: Overrides options for `refresh_cache.apply_async` (e.g. `queue`).
    task_options = None

    #: Cache statuses
    MISS, HIT, STALE = range(3)

    @property
    def class_path(self):
        return '%s.%s' % (self.__module__, self.__class__.__name__)

    def __init__(self):
        self.cache_alias = (self.cache_alias or
                            getattr(settings, 'CACHEBACK_CACHE_ALIAS', DEFAULT_CACHE_ALIAS))
        self.cache = caches[self.cache_alias]
        self.task_options = self.task_options or {}

    def get_init_args(self):
        """
        Return the args that need to be passed to __init__ when
        reconstructing this class.
        """
        return ()

    def get_init_kwargs(self):
        """
        Return the kwargs that need to be passed to __init__ when
        reconstructing this class.
        """
        return {}

    # --------
    # MAIN API
    # --------

    def get(self, *raw_args, **raw_kwargs):
        """
        Return the data for this function (using the cache if possible).

        This method is not intended to be overidden
        """
        # We pass args and kwargs through a filter to allow them to be
        # converted into values that can be pickled.
        args = self.prepare_args(*raw_args)
        kwargs = self.prepare_kwargs(**raw_kwargs)

        # Build the cache key and attempt to fetch the cached item
        key = self.key(*args, **kwargs)
        item = self.cache.get(key)

        call = Call(args=raw_args, kwargs=raw_kwargs)

        if item is None:
            # Cache MISS - we can either:
            # a) fetch the data immediately, blocking execution until
            #    the fetch has finished, or
            # b) trigger an async refresh and return an empty result
            if self.should_missing_item_be_fetched_synchronously(*args, **kwargs):
                logger.debug(("Job %s with key '%s' - cache MISS - running "
                              "synchronous refresh"),
                             self.class_path, key)
                result = self.refresh(*args, **kwargs)
                return self.process_result(
                    result, call=call, cache_status=self.MISS, sync_fetch=True)

            else:
                logger.debug(("Job %s with key '%s' - cache MISS - triggering "
                              "async refresh and returning empty result"),
                             self.class_path, key)
                # To avoid cache hammering (ie lots of identical tasks
                # to refresh the same cache item), we reset the cache with an
                # empty result which will be returned until the cache is
                # refreshed.
                result = self.empty()
                self.store(key, self.timeout(*args, **kwargs), result)
                self.async_refresh(*args, **kwargs)
                return self.process_result(
                    result, call=call, cache_status=self.MISS,
                    sync_fetch=False)

        expiry, data = item
        delta = time.time() - expiry
        if delta > 0:
            # Cache HIT but STALE expiry - we can either:
            # a) fetch the data immediately, blocking execution until
            #    the fetch has finished, or
            # b) trigger a refresh but allow the stale result to be
            #    returned this time.  This is normally acceptable.
            if self.should_stale_item_be_fetched_synchronously(
                    delta, *args, **kwargs):
                logger.debug(
                    ("Job %s with key '%s' - STALE cache hit - running "
                     "synchronous refresh"),
                    self.class_path, key)
                result = self.refresh(*args, **kwargs)
                return self.process_result(
                    result, call=call, cache_status=self.STALE,
                    sync_fetch=True)

            else:
                logger.debug(
                    ("Job %s with key '%s' - STALE cache hit - triggering "
                     "async refresh and returning stale result"),
                    self.class_path, key)
                # We replace the item in the cache with a 'timeout' expiry - this
                # prevents cache hammering but guards against a 'limbo' situation
                # where the refresh task fails for some reason.
                timeout = self.timeout(*args, **kwargs)
                self.store(key, timeout, data)
                self.async_refresh(*args, **kwargs)
                return self.process_result(
                    data, call=call, cache_status=self.STALE, sync_fetch=False)
        else:
            logger.debug("Job %s with key '%s' - cache HIT", self.class_path, key)
            return self.process_result(data, call=call, cache_status=self.HIT)

    def invalidate(self, *raw_args, **raw_kwargs):
        """
        Mark a cached item invalid and trigger an asynchronous
        job to refresh the cache
        """
        args = self.prepare_args(*raw_args)
        kwargs = self.prepare_kwargs(**raw_kwargs)
        key = self.key(*args, **kwargs)
        item = self.cache.get(key)
        if item is not None:
            expiry, data = item
            self.store(key, self.timeout(*args, **kwargs), data)
            self.async_refresh(*args, **kwargs)

    def delete(self, *raw_args, **raw_kwargs):
        """
        Remove an item from the cache
        """
        args = self.prepare_args(*raw_args)
        kwargs = self.prepare_kwargs(**raw_kwargs)
        key = self.key(*args, **kwargs)
        item = self.cache.get(key)
        if item is not None:
            self.cache.delete(key)

    def raw_get(self, *raw_args, **raw_kwargs):
        """
        Retrieve the item (tuple of value and expiry) that is actually in the cache,
        without causing a refresh.
        """

        args = self.prepare_args(*raw_args)
        kwargs = self.prepare_kwargs(**raw_kwargs)

        key = self.key(*args, **kwargs)

        return self.cache.get(key)

    def set(self, *raw_args, **raw_kwargs):
        """
        Manually set the cache value with its appropriate expiry.
        """
        if self.set_data_kwarg in raw_kwargs:
            data = raw_kwargs.pop(self.set_data_kwarg)
        else:
            raw_args = list(raw_args)
            data = raw_args.pop()

        args = self.prepare_args(*raw_args)
        kwargs = self.prepare_kwargs(**raw_kwargs)

        key = self.key(*args, **kwargs)

        expiry = self.expiry(*args, **kwargs)

        logger.debug("Setting %s cache with key '%s', args '%r', kwargs '%r', expiry '%r'",
                     self.class_path, key, args, kwargs, expiry)

        self.store(key, expiry, data)

    # --------------
    # HELPER METHODS
    # --------------

    def prepare_args(self, *args):
        return args

    def prepare_kwargs(self, **kwargs):
        return kwargs

    def store(self, key, expiry, data):
        """
        Add a result to the cache

        :key: Cache key to use
        :expiry: The expiry timestamp after which the result is stale
        :data: The data to cache
        """
        self.cache.set(key, (expiry, data), self.cache_ttl)

        if getattr(settings, 'CACHEBACK_VERIFY_CACHE_WRITE', True):
            # We verify that the item was cached correctly.  This is to avoid a
            # Memcache problem where some values aren't cached correctly
            # without warning.
            __, cached_data = self.cache.get(key, (None, None))
            if data is not None and cached_data is None:
                raise RuntimeError(
                    "Unable to save data of type %s to cache" % (
                        type(data)))

    def refresh(self, *args, **kwargs):
        """
        Fetch the result SYNCHRONOUSLY and populate the cache
        """
        result = self.fetch(*args, **kwargs)
        self.store(self.key(*args, **kwargs), self.expiry(*args, **kwargs), result)
        return result

    def async_refresh(self, *args, **kwargs):
        """
        Trigger an asynchronous job to refresh the cache
        """
        # We trigger the task with the class path to import as well as the
        # (a) args and kwargs for instantiating the class
        # (b) args and kwargs for calling the 'refresh' method

        try:
            enqueue_task(
                dict(
                    klass_str=self.class_path,
                    obj_args=self.get_init_args(),
                    obj_kwargs=self.get_init_kwargs(),
                    call_args=args,
                    call_kwargs=kwargs
                ),
                task_options=self.task_options
            )
        except Exception as e:
            # Handle exceptions from talking to RabbitMQ - eg connection
            # refused.  When this happens, we try to run the task
            # synchronously.
            logger.error("Unable to trigger task asynchronously - failing "
                         "over to synchronous refresh", exc_info=True)
            try:
                return self.refresh(*args, **kwargs)
            except Exception as e:
                # Something went wrong while running the task
                logger.error("Unable to refresh data synchronously: %s", e,
                             exc_info=True)
            else:
                logger.debug("Failover synchronous refresh completed successfully")

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

    def timeout(self, *args, **kwargs):
        """
        Return the refresh timeout for this item
        """
        return time.time() + self.refresh_timeout

    def should_missing_item_be_fetched_synchronously(self, *args, **kwargs):
        """
        Return whether to refresh an item synchronously when it is missing from
        the cache
        """
        return self.fetch_on_miss

    def should_item_be_fetched_synchronously(self, *args, **kwargs):
        import warnings
        warnings.warn(
            "The method 'should_item_be_fetched_synchronously' is deprecated "
            "and will be removed in 0.5.  Use "
            "'should_missing_item_be_fetched_synchronously' instead.",
            DeprecationWarning)
        return self.should_missing_item_be_fetched_synchronously(
            *args, **kwargs)

    def should_stale_item_be_fetched_synchronously(self, delta, *args, **kwargs):
        """
        Return whether to refresh an item synchronously when it is found in the
        cache but stale
        """
        if self.fetch_on_stale_threshold is None:
            return False
        return delta > (self.fetch_on_stale_threshold - self.lifetime)

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
                return "%s:%s" % (self.class_path, self.hash(args))
            # The line might break if your passed values are un-hashable.  If
            # it does, you need to override this method and implement your own
            # key algorithm.
            return "%s:%s:%s:%s" % (self.class_path,
                                    self.hash(args),
                                    self.hash([k for k in sorted(kwargs)]),
                                    self.hash([kwargs[k] for k in sorted(kwargs)]))
        except TypeError:
            raise RuntimeError(
                "Unable to generate cache key due to unhashable"
                "args or kwargs - you need to implement your own"
                "key generation method to avoid this problem")

    def hash(self, value):
        """
        Generate a hash of the given iterable.

        This is for use in a cache key.
        """
        if is_iterable(value):
            value = tuple(to_bytestring(v) for v in value)
        return hashlib.md5(six.b(':').join(value)).hexdigest()

    def fetch(self, *args, **kwargs):
        """
        Return the data for this job - this is where the expensive work should
        be done.
        """
        raise NotImplementedError()

    def process_result(self, result, call, cache_status, sync_fetch=None):
        """
        Transform the fetched data right before returning from .get(...)

        :param result: The result to be returned
        :param call: A named tuple with properties 'args' and 'kwargs that
                     holds the call args and kwargs
        :param cache_status: A status integrer, accessible as class constants
                             self.MISS, self.HIT, self.STALE
        :param sync_fetch: A boolean indicating whether a synchronous fetch was
                           performed. A value of None indicates that no fetch
                           was required (ie the result was a cache hit).
        """
        return result

    # --------------------
    # ASYNC HELPER METHODS
    # --------------------

    @classmethod
    def job_refresh(cls, *args, **kwargs):
        warnings.warn(
            '`Job.job_refresh` is deprecated, use `perform_async_refresh` instead.',
            RemovedInCacheback13Warning
        )
        return cls.perform_async_refresh(*args, **kwargs)

    @classmethod
    def perform_async_refresh(cls, klass_str, obj_args, obj_kwargs, call_args, call_kwargs):
        """
        Re-populate cache using the given job class.

        The job class is instantiated with the passed constructor args and the
        refresh method is called with the passed call args.  That is::

            data = klass(*obj_args, **obj_kwargs).refresh(
                *call_args, **call_kwargs)

        :klass_str: String repr of class (eg 'apps.twitter.jobs.FetchTweetsJob')
        :obj_args: Constructor args
        :obj_kwargs: Constructor kwargs
        :call_args: Refresh args
        :call_kwargs: Refresh kwargs
        """
        klass = get_job_class(klass_str)
        if klass is None:
            logger.error("Unable to construct %s with args %r and kwargs %r",
                         klass_str, obj_args, obj_kwargs)
            return

        logger.info("Using %s with constructor args %r and kwargs %r",
                    klass_str, obj_args, obj_kwargs)
        logger.info("Calling refresh with args %r and kwargs %r", call_args,
                    call_kwargs)
        start = time.time()
        try:
            klass(*obj_args, **obj_kwargs).refresh(
                *call_args, **call_kwargs)
        except Exception as e:
            logger.exception("Error running job: '%s'", e)
        else:
            duration = time.time() - start
            logger.info("Refreshed cache in %.6f seconds", duration)
