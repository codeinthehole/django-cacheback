=========
Cacheback
=========
----------------------------------------
Asynchronous cache refreshing for Django
----------------------------------------

What does this library do?
--------------------------
It's an extensible caching library that refreshes stale cache items
asynchronously using a Celery_ task.  The key idea being that it's
better to serve a stale item (and populate the cache asynchronously) than block
the user in order to populate the cache synchronously.

.. _Celery: http://celeryproject.org/

Using this library, you can structure your views so that all reads are from
cache - this can be a significant performance boost.  

A corollary of this technique is that cache hammering can be handled simply and
elegantly, avoiding suddent surges of expensive reads when a cached items becomes stale.

Can I use this in my project?
-----------------------------
Yes, subject to the `MIT license`_.

.. _`MIT license`: https://github.com/codeinthehole/django-cacheback/blob/master/LICENSE

How do I install?
-----------------
Fetch from PyPI::

    pip install django-cacheback

and add ``cacheback`` to ``INSTALLED_APPS``.  Since Celery is a dependency, you
will also need to set up a broker.

I want to contribute
--------------------
Get set up by cloning, creating a virtualenv and running::

    make develop

to install the dependencies.

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
