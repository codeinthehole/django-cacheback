Advanced usage
--------------

Two thresholds for cache invalidation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's possible to employ two threshold times for cache behaviour:

1.  A time after which the cached item is considered 'stale'.  When a stale item
    is returned, a async job is triggered to refresh the item but the stale item
    is returned.  This is controlled by the ``lifetime`` attribute of the
    ``Job`` class - the default value is 600 seconds (5 minutes).

2.  A time after which the cached item is removed (a cache miss).  If you have
    ``fetch_on_miss=True``, then this will trigger a synchronous data fetch.
    This is controlled by the ``cache_ttl`` attribute of the ``Job`` class - the
    default value is 2592000 seconds, which is the maximum ttl that memcached
    supports.

