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
