==================
Django-async-cache
==================

What does this library do?
==========================
It provides a caching mechanism that populates the cache asynchronously, using
Celery.  

I don't get it...
=================


What's the point?
=================
It allows your views to do all their reads from the cache - all cache updates
take place offline.  This can be a significant performance increase.

Show me an example
==================
Ok, bossy-boots.

A library that provides caching where the stale cache items are refreshed using
asynchronously, using Celery.

Simple example::

    def fetch_tweets(username):
        ... # Expensive work happens here
        return tweets

Can I use this in my project?
=============================
Yes, subject to the `MIT license`_.

.. _`MIT license`: http://example.com

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
