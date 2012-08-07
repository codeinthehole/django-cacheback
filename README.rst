=========
Cacheback
=========
-----------------------------------------
Asynchronous cache refreshing for Django.
-----------------------------------------

This library allows you to fetch all your reads from cache, using a Celery task
to refresh the cache when items becomes stale. 

Questions
=========

What does this library do?
--------------------------
It provides a caching mechanism that populates the cache asynchronously using a
Celery worker.  It allows you to structure your views so that all reads are from
cache - this can be a significant performance boost.

I don't get it...
-----------------
User makes request, we look in cache for the result

1. Cache MISS - we return an empty result set.  This can be configured to
   perform a synchronous read if returning an empty result set is unacceptable.
2. Cache HIT with a valid result - return result.
3. Cache HIT but with a stale result - we trigger a job to refresh this cache
   item but return the stale item.

The key thing to note is that we do allow stale results to be returned.  This is
normally an acceptable trade-off for the performance benefits that this library
provides.

Show me an example
------------------
Ok, bossy-boots.  Suppose you have a view which makes an expensive read::

    from django.shortcuts import render
    import twitter # fictional library

    def show_tweets(request, username):
        tweets = twitter.user_tweets(username)
        return render(request, 'tweets.html', 
                      {'tweets': tweets})

where the call to ``user_tweets`` is expensive.  You can introduce
asynchronous caching by creating a simple class that wraps the read operation::

    import cacheback
    import twitter

    class UserTweets(cacheback.AsyncCacheJob):
        lifetime = 600 # Cache for 10 minutes
        
        def fetch(self, username):
            return twitter.user_tweets(username)

Now your view can be rewritten as::

    from django.shortcuts import render
    from jobs import UserTweets

    def show_tweets(request, username):
        tweets = UserTweets.get(username)
        return render(request, 'tweets.html', 
                      {'tweets': tweets})

Now all requests will read tweets from cache - when the cached items expire,
they will be refreshed asynchronously.

Can I use this in my project?
-----------------------------
Yes, subject to the `MIT license`_.

.. _`MIT license`: http://example.com

How do I install?
-----------------
Fetch from PyPI::

    pip install django-cacheback

and add ``cacheback`` to ``INSTALLED_APPS``.

I want to contribute
--------------------
Get set up by cloning, creating a virtualenv and running::

    make develop

Running tests
~~~~~~~~~~~~~
Use::

    ./runtests.py

Sandbox VM
~~~~~~~~~~

There is a VagrantFile for setting up a sandbox VM where you can play around
with the functionality.  First install the necessary puppet modules::

    make puppet

then boot and provision the VM::

    vagrant up

This may take a while but will set up a Ubuntu Precise64 VM with RabbitMQ
installed and configured.  You can then SSH into the machine and run the Django
development server::

    vagrant ssh
    cd /vagrant/sandbox
    source /var/www/virtual/bin/activate
    ./manage.py runserver 0.0.0.0:8000

The dummy site will be available at ``localhost:8080``.

Run a Celery worker using::

    ./manage.py celeryctl worker --loglevel=INFO
