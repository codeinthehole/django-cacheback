============
Sample usage
============

As a decorator
~~~~~~~~~~~~~~

Simply wrap the function whose results you want to cache::

    import requests
    from cacheback.decorators import cacheback

    @cacheback()
    def fetch_tweets(username):
        url = "https://twitter.com/statuses/user_timeline.json?screen_name=%s"
        return requests.get(url % username).json

The default behaviour of the ``cacheback`` decorator is to:

* Cache items for 10 minutes.

* When the cache is empty for a given key, the data will be fetched
  synchronously.

You can parameterise the decorator to cache items for longer and also to not block on a
cache miss::

    import requests
    from cacheback.decorators import cacheback

    @cacheback(lifetime=1200, fetch_on_miss=False)
    def fetch_tweets(username):
        url = "https://twitter.com/statuses/user_timeline.json?screen_name=%s"
        return requests.get(url % username).json

Now:

* Items will be cached for 20 minutes;

* For a cache miss, ``None`` will be returned and the cache refreshed
  asynchronously.

As an instance of ``cacheback.Job``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Subclassing ``cacheback.Job`` gives you complete control over the caching
behaviour.  The only method that must be overridden is ``fetch`` which is
responsible for fetching the data to be cached::

    import requests
    from cacheback.base import Job

    class UserTweets(Job):

        def fetch(self, username):
            url = "https://twitter.com/statuses/user_timeline.json?screen_name=%s"
            return requests.get(url % username).json

Client code only needs to be aware of the ``get`` method which returns the
cached data.  For example::

    from django.shortcuts import render

    def tweets(request, username):
        return render(request,
                      'tweets.html',
                      {'tweets': UserTweets().get(username)})

You can control the lifetime and behaviour on cache miss using either class
attributes::

    import requests
    from cacheback.base import Job

    class UserTweets(Job):
        lifetime = 60*20
        fetch_on_miss = False

        def fetch(self, username):
            url = "https://twitter.com/statuses/user_timeline.json?screen_name=%s"
            return requests.get(url % username).json

or by overriding methods::

    import time
    import requests
    from cacheback.base import Job

    class UserTweets(Job):

        def fetch(self, username):
            url = "https://twitter.com/statuses/user_timeline.json?screen_name=%s"
            return requests.get(url % username).json

        def expiry(self, username):
            now = time.time()
            if username.startswith(a):
                return now + 60*20
            return now + 60*10

        def should_item_be_fetched_synchronously(self, username):
            return username.startswith(a)

In the above toy example, the cache behaviour will be different for usernames
starting with 'a'.

Invalidation
~~~~~~~~~~~~

If you want to programmatically invalidate a cached item, use the ``invalidate``
method on a job instance::

    job = UserTweets()
    job.invalidate(username)

This will trigger a new asynchronous refresh of the item.

You can also simply remove an item from the cache so that the next request will
trigger the refresh::

    job.delete(username)

Setting cache values
~~~~~~~~~~~~~~~~~~~~

If you want to update the cache programmatically use the ``set`` method on
a job instance (this can be useful when your program can discover updates through a
separate mechanism for example, or for caching partial or derived data)::

    tweets_job = UserTweets()

    user_tweets = tweets_job.get(username)

    new_tweet = PostTweet(username, 'Trying out Cacheback!')

    # Naive example, assuming no other process would have updated the tweets
    tweets_job.set(username, user_tweets + [new_tweet])

The data to be cached can be specified in a few ways. Firstly it can be the last
positional argument, as above. If that is unclear, you can also use the keyword ``data``::

    tweets_job.set(username, data=(current_tweets + [new_tweet]))

And if your cache method already uses a keyword argument called ``data`` you can specify
the name of a different parameter as a class variable called ``set_data_kwarg``::

    class CustomKwUserTweets(UserTweets):
        set_data_kwarg = 'my_cache_data'

    custom_tweets_job = CustomKwUserTweets()

    custom_tweets_job.set(username, my_cache_data=(user_tweets + [new_tweet]))

This also works with a decorated function::

    @cacheback()
    def fetch_tweets(username):
        url = "https://twitter.com/statuses/user_timeline.json?screen_name=%s"
        return requests.get(url % username).json

    user_tweets = fetch_tweets(username)

    new_tweet = PostTweet(username, 'Trying out Cacheback!')

    fetch_tweets.job.set(fetch_tweets, username, (user_tweets + [new_tweet])))

or::

    fetch_tweets.job.set(fetch_tweets, username, data=(current_tweets + [new_tweet])))

And you can specify the ``set_data_kwarg`` in the decorator params as you'd expect::

    @cacheback(set_data_kwarg='my_cache_data')
    def fetch_tweets(username):
        url = "https://twitter.com/statuses/user_timeline.json?screen_name=%s"
        return requests.get(url % username).json

    fetch_tweets.job.set(fetch_tweets, username, my_cache_data=(user_tweets + [new_tweet])))

**NOTE:** If your ``fetch`` method, or cacheback-decorated function takes a named parameter
of ``data`` and you wish to use the ``set`` method, you **must** provide a new value for the
``set_data_kwarg`` parameter, and not pass in the data to cache as the last positional argument.
Otherwise the value of the ``data`` parameter will be used as the data to cache.


Checking what's in the cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
On occasion you may wish to check exactly what Cacheback has stored in the cache without triggering a refresh — this is ususally useful for seeing if values have updated since the last time they were retrieved. The ``raw_get`` method allows you to do that, and uses the same semantics as ``get``, ``set``, etc. It returns the value that's actually stored in the cache, i.e., the ``(expiry, data)`` tuple, or ``None`` if no value has yet been set::


    # Don't want to trigger a refetch at this point
    raw_cache_value = fetch_tweets.job.raw_get(fetch_tweets, username)

    if raw_cache_value is not None:
        expiry, cached_tweets = raw_cache_value


Post-processing
~~~~~~~~~~~~~~~

The ``cacheback.Job`` instance provides a `process_result` method that can be
overridden to modify the result value being returned. You can use this to append
information about whether the result is being returned from cache or not.
