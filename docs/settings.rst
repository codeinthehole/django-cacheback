========
Settings
========

``CACHEBACK_CACHE_ALIAS``
-------------------------

This specifies which cache to use from your ``CACHES`` setting. It defaults to
``default``.


``CACHEBACK_VERIFY_CACHE_WRITE``
--------------------------------

This verifies the data is correctly written to memcache. If not, then a
``RuntimeError`` is raised. Defaults to ``True``.


``CACHEBACK_TASK_QUEUE``
------------------------

This defines the task queue to use. Valid options are ``rq`` and ``celery``.
Make sure that the corresponding task queue is configured too.


``CACHEBACK_TASK_IGNORE_RESULT``
--------------------------------

This specifies whether to ignore the result of the ``refresh_cache`` task
and prevent Celery/RQ from storing it into its results backend.


``CACHEBACK_VALIDATE_JOB_REFRESH_NEEDED``
-----------------------------------------

When enabled, the async refresh task verifies the cached value's expiry
before running and skips the refresh if the cached value still has more
than ``refresh_timeout`` seconds remaining before its expiry. This avoids
redundant work when refresh tasks for the same key pile up in a slow
worker queue: once one of them refreshes the cache, the remaining tasks
short-circuit instead of re-fetching the same data.

The ``refresh_timeout`` margin ensures that tasks are still allowed to
run when the cache is about to expire, so a stale value isn't served
because the next refresh was skipped too eagerly.

Defaults to ``False`` to preserve the previous behavior of always
refreshing when a task is picked up.
