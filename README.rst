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


Supported versions
------------------

Python 3.10+ is supported. Django 5.2+ is supported.


Do you have tests?
------------------

You betcha!

.. image:: https://github.com/codeinthehole/django-cacheback/workflows/CI/badge.svg?branch=master
     :target: https://github.com/codeinthehole/django-cacheback/actions?workflow=CI
     :alt: CI Status


Can I use this in my project?
-----------------------------

Probably - subject to the `MIT license`_.

.. _`MIT license`: https://github.com/codeinthehole/django-cacheback/blob/master/LICENSE


I want to contribute!
---------------------

Brilliant!  Here are the `contributing guidelines`_.

.. _`contributing guidelines`: http://django-cacheback.readthedocs.org/en/latest/contributing.html
