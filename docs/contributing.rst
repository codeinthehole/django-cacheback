============
Contributing
============

Start by cloning the repo, creating a virtualenv and running::

    $ make install

to install the testing dependencies.

Running tests
=============

Use::

    $ py.test

or generate coverage report::

    $ py.test --cov=cacheback

or use Tox with::

    $ tox

to test all Python/Django combinations.

Sandbox VM
==========

There is a ``VagrantFile`` for setting up a sandbox VM where you can play around
with the functionality.  Bring up the Vagrant box::

    $ vagrant up

This may take a while but will set up a Ubuntu Precise64 VM with RabbitMQ
installed.  You can then SSH into the machine::

    $ vagrant ssh
    $ cd /vagrant/sandbox

You can now decide to run the Celery implementation::

    $ honcho -f Procfile.celery start

Or you can run the RQ implementation::

    $ honcho -f Procfile.rq start

The above commands will start a Django runserver and the selected task worker.
The dummy site will be available at ``http://localhost:8080`` on your host
machine.  There are some sample views in ``sandbox/dummyapp/views.py`` that
exercise django-cacheback.
