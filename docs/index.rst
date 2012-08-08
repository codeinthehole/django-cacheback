.. django-async-cache documentation master file, created by
   sphinx-quickstart on Mon Jul 30 21:40:46 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Asynchronous cache refreshing for Django
========================================

Usage
-----

The simplest way to use the library is to subclass the
``async_cache.AsyncCacheJob`` class and override the ``fetch`` method to fetch
the data in question.

.. autoclass:: async_cache.AsyncCacheJob
    :members: 

Examples::

    import requests
    from async_cache import AsyncCacheJob
    import simplejson

    class UserTweets(AsyncCacheJob):
        ttl = 60
        
        def fetch(self, username):
            url = "https://twitter.com/statuses/user_timeline.json?screen_name=%s" % username
            response = requests.get(url)
            response simplejson.loads(response.content)

This could be then used in a view::

    from django.shortcuts import render

    def view(request, username):
        return render(request, 'tweets.html',
                      {'tweets': UserTweets().get(username)})

Now all reads will come from the cache.  When a cached result is stale (more
than 60 seconds old), a cache refresh job will be triggered and a Celery task
will update the cache.

Queryset jobs
-------------

There are two classes for easy caching of ORM reads.  These don't need
subclassing but rather take the model class as a ``__init__`` parameter.

.. autoclass:: async_cache.QuerySetFilterJob
    :members:

.. autoclass:: async_cache.QuerySetGetJob
    :members:

Example usage::
 
    from django.contrib.auth import models
    from django.shortcuts import render
    from async_cache import QuerySetGetJob, QuerySetFilterJob

    def user_detail(request, username):
        user = QuerySetGetJob(models.User).get(username=username)
        return render(request, 'user.html',
                      {'user': user})

    def staff(request):
        staff = QuerySetFilterJob(models.User).filter(is_staff=True)
        return render(request, 'staff.html',
                      {'users': staff})

These classes are helpful for simple ORM reads but won't be suitable for more
complicated queries where ``filter`` is chained together with ``exclude``.

Advanced usage
--------------

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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

