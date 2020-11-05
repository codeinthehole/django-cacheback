Advanced usage
--------------

Three thresholds for cache invalidation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's possible to employ three threshold times to control cache behaviour:

1.  A time after which the cached item is considered 'stale'.  When a stale item
    is returned, an async job is triggered to refresh the item but the stale item
    is returned.  This is controlled by the ``lifetime`` attribute of the
    ``Job`` class - the default value is 600 seconds (10 minutes).

2.  A time after which the cached item is removed (a cache miss).  If you have
    ``fetch_on_miss=True``, then this will trigger a synchronous data fetch.
    This is controlled by the ``cache_ttl`` attribute of the ``Job`` class - the
    default value is 2592000 seconds, which is the maximum ttl that memcached
    supports.

3.  A timeout value for the refresh job.  If the cached item is not refreshed
    after this time, then another async refresh job will be triggered.  This is
    controlled by the ``refresh_timeout`` attribute of the ``Job`` class and
    defaults to 60 seconds.
