==================
Django-async-cache
==================

Asynchronous cache refreshing using Celery.

**This is a work in progress**

What does this library do?
==========================
It provides a caching mechanism that populates the cache asynchronously using
Celery.  It allows you to structure your views so that all reads from cache.
This can be a significant performance boost.

I don't get it...
=================

1. User makes request, we look in cache for the result
   a) Cache MISS - we return an empty result set
   b) Cache HIT with a valid result which is returned
   c) Cache HIT but result is stale - we trigger a job to refresh this cache
   item but return the stale item

What's the point?
=================
It allows your views to do all their reads from the cache - all cache updates
take place offline.  This can be a significant performance increase.

Show me an example
==================
Ok, bossy-boots.  Suppose you have a view which makes an expensive read::

    from django.shortcuts import render
    import twitter # fictional library

    def show_tweets(request, username):
        tweets = twitter.user_tweets(username)
        return render(request, 'tweets.html', 
                      {'tweets': tweets})

Suppose the call to ``user_tweets`` takes around 3 seconds.  You can introduce
asynchronous caching by creating a simple class::

    from async_cache import AsyncCacheJob
    import twitter

    class UserTweets(AsyncCacheJob):
        
        def fetch(self, username):
            return twitter.user_tweets(username)

Now your view can be rewritten as::

    from django.shortcuts import render
    from jobs import UserTweets

    def show_tweets(request, username):
        tweets = UserTweets.get(username)
        return render(request, 'tweets.html', 
                      {'tweets': tweets})

Now all requests will read tweets from cache - all refreshs will be done
asynchronously.

Can I use this in my project?
=============================
Yes, subject to the `MIT license`_.

.. _`MIT license`: http://example.com

How do I install?
=================

1. Add ``async_cache`` to ``INSTALLED_APPS``.
2. Set-up Celery 

I've found a bug
================
No you haven't.

I want to contribute
====================
There is a VagrantFile for setting up a testing VM.  First install puppet
modules::

    make puppet

then boot and provision the VM::

    vagrant up

This will set up a Ubuntu Precise64 VM with RabbitMQ installed and configured.

Vagrant is awesome btw
