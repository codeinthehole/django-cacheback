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

* Cache items for 5 minutes.  

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
