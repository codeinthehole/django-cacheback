.. django-async-cache documentation master file, created by
   sphinx-quickstart on Mon Jul 30 21:40:46 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================================================
Django Cacheback - asynchronous cache refreshing
================================================

Cacheback is a caching library that uses Celery to refresh stale cached items
asynchronously.  The key idea being that it is better to serve a stale cache
item than fetch the data synchronously.  Populating the cache asynchronously
allows your views to be adjusted so all reads come from cache.  It also handles
cache hammering gracefully.

Cacheback provides a decorator for simple usage and provides a subclassable base
class for more fine-grained control.

Simple example
--------------
Suppose you have a view which displays a user's tweets, something like::

    from django.shortcuts import render
    import requests

    def show_tweets(request, username):
        url = "https://twitter.com/statuses/user_timeline.json?screen_name=%s"
        response = requests.get(url % username)
        return render(request, 'tweets.html', {'tweets': response.json})

The HTTP round-trip to Twitter is expensive.  We want to use some caching to
improve performance.  

A better solution is to use Cacheback::

    from django.shortcuts import render
    import requests
    from cacheback import cacheback

    @cacheback(1200)
    def fetch_tweets(username):
        url = "https://twitter.com/statuses/user_timeline.json?screen_name=%s"
        return requests.get(url % username).json
        
    def show_tweets(request, username):
        return render(request, 'tweets.html', {'tweets': fetch_tweets(username)})

The behaviour of this implementation is as follows:

* The first request for a particular user's tweets will fetch the tweet data
  synchronously as the cache will be empty.  

* Any subsequent requests within 1200 seconds will be served straight from
  cache.

* The first request after 1200 seconds will serve the (now-stale) cache result
  but will trigger a Celery task to fetch the user's tweets and repopulate the
  cache.

* Any requests the arrive after this request but before the cache has been
  refreshed will return the stale result.

Much of this behaviour can be configured.  Note that the initial synchronous
fetch can be avoided by passing ``fetch_on_miss=False`` to the decorator.  This will
lead to an empty result being returned for the first request with an
asynchronous job populating the cache.

Install
-------
Run::

    pip install django-cacheback

Examples
--------

Example 1 - Decorate
~~~~~~~~~~~~~~~~~~~~
Extract the data fetching into a function and decorate::

    from django.shortcuts import render
    import requests
    from cacheback import cacheback

    @cacheback()
    def fetch_tweets(username):
        url = "https://twitter.com/statuses/user_timeline.json?screen_name=%s"
        return requests.get(url % username).json
        
    def show_tweets(request, username):
        return render(request, 'tweets.html', {'tweets': fetch_tweets(username)})

The default behaviour of the ``cacheback`` decorator is to:

* Cache items for 5 minutes.  After that, they will be considered stale and a
  job will be triggered to refresh the cache.

* When the cache is empty for a given key, the data will be fetched
  synchronously.  This behaviour can be changed so that the read never blocks -
  see later.
    
Example 2 - Decorate plus
~~~~~~~~~~~~~~~~~~~~~~~~~~
You can tweak the decorator to cache items for longer and also to not block on a
cache miss::

    from django.shortcuts import render
    import requests
    from cacheback import cacheback

    @cacheback(1200, fetch_on_miss=False)
    def fetch_tweets(username):
        url = "https://twitter.com/statuses/user_timeline.json?screen_name=%s"
        return requests.get(url % username).json
        
    def show_tweets(request, username):
        return render(request, 'tweets.html', {'tweets': fetch_tweets(username)})
    
Example 3 - Subclassing for greater control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Subclassing ``cacheback.Job`` gives you complete control over the caching
behaviour::

    import requests
    from cacheback import Job

    class UserTweets(Job):
        
        def fetch(self, username):
            url = "https://twitter.com/statuses/user_timeline.json?screen_name=%s"
            return requests.get(url % username).json

        def lifetime(self, username):
            return 1200 if username.startswith('a') else 600

API
---

.. autoclass:: cacheback.Job
    :members: fetch, empty, expiry, key, prepare_args, prepare_kwargs


Queryset jobs
-------------

There are two classes for easy caching of ORM reads.  These don't need
subclassing but rather take the model class as a ``__init__`` parameter.

.. autoclass:: cacheback.QuerySetFilterJob
    :members:

.. autoclass:: cacheback.QuerySetGetJob
    :members:

Example usage::
 
    from django.contrib.auth import models
    from django.shortcuts import render
    from cacheback import QuerySetGetJob, QuerySetFilterJob

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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

