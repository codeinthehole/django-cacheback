=========
Changelog
=========

1.3.1
~~~~~

* Add support for Django 1.11.

1.3
~~~
* Add set method, with the same semantics as delete & get. Updated docs.

1.2
~~~

* Add support for Django 1.10 (and drop support for Django < 1.8)
* Refactored codebase, cleaned up method naming and module structure. Old imports
  and methods will work at least for this release. RemovedInCacheback13Warning is
  set if old methods or imports are used.
* Add option to have a different cache per cacheback job

1.1
~~~

* Added support for multiple background workers (currently Celery and rq)
* Add pytest support

1.0
~~~
* Support Django versions >= 1.7
* Update sandbox to work with Django 1.9

0.9.1
~~~~~
* Fix silly ``NameError`` introduced in 0.9 (`#39`)

.. _`#39`: https://github.com/codeinthehole/django-cacheback/pull/39

0.9
~~~
* Add support for other caches (`#32`_)
* Fix inconsistent hasing issue in Python 3.x (`#28`_)
* Allow ``job_class_kwargs`` to be passed to ``cacheback`` decorator (`#31`_)

.. _`#32`: https://github.com/codeinthehole/django-cacheback/pull/32
.. _`#28`: https://github.com/codeinthehole/django-cacheback/pull/28
.. _`#31`: https://github.com/codeinthehole/django-cacheback/pull/31

0.8
~~~
* Add support for Python 3 (`#24`_)

.. _`#24`: https://github.com/codeinthehole/django-cacheback/pull/24

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
