=========
Cacheback
=========
----------------------------------------
Asynchronous cache refreshing for Django
----------------------------------------

What does this library do?
--------------------------
It's an extensible caching library that refreshes stale cache items
asynchronously using a Celery_ or rq_ task (utilizing django-rq). The key
idea being that it's better to serve a stale item (and populate the cache
asynchronously) than block the response process in order to populate the cache
synchronously.

.. _Celery: http://celeryproject.org/
.. _rq: http://python-rq.org/

Using this library, you can rework your views so that all reads are from
cache - which can be a significant performance boost.

A corollary of this technique is that cache hammering can be handled simply and
elegantly, avoiding sudden surges of expensive reads when a cached item becomes stale.

Do you have good docs?
----------------------
Yup - `over on readthedocs.org`_.

.. _`over on readthedocs.org`: http://django-cacheback.readthedocs.org/en/latest/

Do you support Python 3?
------------------------
Pythons 2.7, 3.3, 3.4, 3.5 and PyPy are supported.

Django versions 1.8 to 1.11 are supported.

Do you have tests?
------------------
You betcha!

.. image:: https://secure.travis-ci.org/codeinthehole/django-cacheback.png
    :target: https://travis-ci.org/#!/codeinthehole/django-cacheback

Can I use this in my project?
-----------------------------
Probably - subject to the `MIT license`_.

.. _`MIT license`: https://github.com/codeinthehole/django-cacheback/blob/master/LICENSE

I want to contribute!
---------------------
Brilliant!  Here are the `contributing guidelines`_.

.. _`contributing guidelines`: http://django-cacheback.readthedocs.org/en/latest/contributing.html
