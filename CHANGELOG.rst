=========
Changelog
=========

0.7
~~~
* Include the class name and module path in the cache key by defauly (`#21`_)

.. _`#21`: https://github.com/codeinthehole/django-cacheback/pull/21

0.6
~~~
* Celery task arguments can now be passed (`#20`_).
* Include reference to job instance on decorator function (`#17`_).  This allows
  caches to be invalidated using the decorator function instance.

.. _`#17`: https://github.com/codeinthehole/django-cacheback/pull/17
.. _`#20`: https://github.com/codeinthehole/django-cacheback/pull/20

0.5
~~~
* Added hook for performing a synchronous refresh of stale items
* Updated docs for invalidation

0.4
~~~
* Handle some error cases
* Add invalidate method

0.3
~~~
* Fixed nasty bug where caching could find it's way into a limbo state (#5)
* Remove bug where it was assumed that cached items would be iterable (#4)
* Added handling of uncacheable types

.. _`#5`: https://github.com/codeinthehole/django-cacheback/pull/5
.. _`#4`: https://github.com/codeinthehole/django-cacheback/pull/4

0.2
~~~
* Docs? Docs!
* Added method for determining whether to "fetch on miss"

0.1
~~~
Minimal viable product
