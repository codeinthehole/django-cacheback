.. django-async-cache documentation master file, created by
   sphinx-quickstart on Mon Jul 30 21:40:46 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================
Django Cacheback
================

Cacheback is an extensible caching library that refreshes stale cache items
asynchronously using a Celery_ or rq_ task (utilizing django-rq).  The key
idea being that it's better to serve a stale item (and populate the cache
asynchronously) than block the response process in order to populate the cache
synchronously.

.. _Celery: http://celeryproject.org/
.. _rq: http://python-rq.org/

Using this library, you can rework your views so that all reads are from
cache - which can be a significant performance boost.  

A corollary of this technique is that cache stampedes can be easily avoided,
avoiding sudden surges of expensive reads when cached items becomes stale.

Cacheback provides a decorator for simple usage, a subclassable base
class for more fine-grained control and helper classes for working with
querysets.

Example
=======

Consider a view for showing a user's tweets:

.. sourcecode:: python

    from django.shortcuts import render
    from myproject.twitter import fetch_tweets

    def show_tweets(request, username):
        return render(request, 'tweets.html', 
                      {'tweets': fetch_tweets(username)})

This works fine but the ``fetch_tweets`` function involves a HTTP round-trip and
is slow.  

Performance can be improved by using Django's `low-level cache API`_:

.. _`low-level cache API`: https://docs.djangoproject.com/en/dev/topics/cache/?from=olddocs#the-low-level-cache-api
        
.. sourcecode:: python

    from django.shortcuts import render
    from django.cache import cache
    from myproject.twitter import fetch_tweets

    def show_tweets(request, username):
        return render(request, 'tweets.html', 
                      {'tweets': fetch_cached_tweets(username)})

    def fetch_cached_tweets(username):
        tweets = cache.get(username)
        if tweets is None:
            tweets = fetch_tweets(username)
            cache.set(username, tweets, 60*15)
        return tweets

Now tweets are cached for 15 minutes after they are first fetched, using the
twitter username as a key.  This is obviously a performance improvement but the
shortcomings of this approach are:

* For a cache miss, the tweets are fetched synchronously, blocking code execution
  and leading to a slow response time.

* This in turn exposes the view to a '`cache stampede`_' where
  multiple expensive reads run simultaneously when the cached item expires.
  Under heavy load, this can bring your site down and make you sad.

.. _`cache stampede`: http://en.wikipedia.org/wiki/Cache_stampede

Now, consider an alternative implementation that uses a Celery task to repopulate the
cache asynchronously instead of during the request/response cycle:

.. sourcecode:: python

    import datetime
    from django.shortcuts import render
    from django.cache import cache
    from myproject.tasks import update_tweets

    def show_tweets(request, username):
        return render(request, 'tweets.html', 
                      {'tweets': fetch_cached_tweets(username)})

    def fetch_cached_tweets(username):
        item = cache.get(username)
        if item is None:
            # Scenario 1: Cache miss - return empty result set and trigger a refresh
            update_tweets.delay(username, 60*15)
            return []
        tweets, expiry = item
        if expiry > datetime.datetime.now():
            # Scenario 2: Cached item is stale - return it but trigger a refresh
            update_tweets.delay(username, 60*15)
        return tweets

where the ``myproject.tasks.update_tweets`` task is implemented as:

.. sourcecode:: python

    import datetime
    from celery import task
    from django.cache import cache
    from myproject.twitter import fetch_tweets

    @task()
    def update_tweets(username, ttl):
        tweets = fetch_tweets(username)
        now = datetime.datetime.now()
        cache.set(username, (tweets, now+ttl), 2592000) 

Some things to note:

* Items are stored in the cache as tuples ``(data, expiry_timestamp)`` using
  Memcache's maximum expiry setting (2592000 seconds).  By using this value, we
  are effectively bypassing memcache's replacement policy in favour of our own.

* As the comments indicate, there are two scenarios to consider:

  1.  Cache miss.  In this case, we don't have any data (stale or otherwise) to
      return.  In the example above, we trigger an asynchronous refresh and
      return an empty result set.  In other scenarios, it may make sense to
      perform a synchronous refresh.

  2.  Cache hit but with stale data.  Here we return the stale data but trigger
      a Celery task to refresh the cached item.

This pattern of re-populating the cache asynchronously works well.  Indeed, it
is the basis for the cacheback library.

Here's the same functionality implemented using a django-cacheback decorator:

.. sourcecode:: python

    from django.shortcuts import render
    from django.cache import cache
    from myproject.twitter import fetch_tweets
    from cacheback.decorators import cacheback

    def show_tweets(request, username):
        return render(request, 'tweets.html', 
                      {'tweets': cacheback(60*15, fetch_on_miss=False)(fetch_tweets)(username)})

Here the decorator simply wraps the ``fetch_tweets`` function - nothing else is
needed.  Cacheback ships with a flexible Celery task that can run any function
asynchronously.

To be clear, the behaviour of this implementation is as follows:

* The first request for a particular user's tweets will be a cache miss.  The
  default behaviour of Cacheback is to fetch the data synchronously in this
  situation, but by passing ``fetch_on_miss=False``, we indicate that it's ok
  to return ``None`` in this situation and to trigger an asynchronous refresh.

* A Celery worker will pick up the job to refresh the cache for this user's
  tweets.  If will import the ``fetch_tweets`` function and execute it with the
  correct username.  The resulting data will be added to the cache with a
  lifetime of 15 minutes.

* Any requests for this user's tweets during the period that Celery is
  refreshing the cache will also return ``None``.  However Cacheback is aware of
  cache stampedes and does not trigger any additional jobs for refreshing the
  cached item.

* Once the cached item is refreshed, any subsequent requests within the next 15
  minutes will be served from cache.

* The first request after 15 minutes has elapsed will serve the (now-stale)
  cache result but will trigger a Celery task to fetch the user's tweets and
  repopulate the cache.

Much of this behaviour can be configured by using a subclass of
``cacheback.Job``.  The decorator is only intended for simple use-cases.  See
the :doc:`usage` and :doc:`api` documentation for more information.

All of the worker related things above an also be done using rq instead of
Celery.

Contents
========

.. toctree::
   :maxdepth: 2

   installation
   usage
   api
   settings
   advanced
   contributing



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

