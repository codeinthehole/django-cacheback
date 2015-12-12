============
Contributing
============

Start by cloning the repo, creating a virtualenv and running::

    $ make

to install the testing dependencies.

Running tests
=============

Use::

    $ ./runtests.py

or use Tox with::

    $ tox

to test all Python/Django combinations.

Sandbox VM
==========

There is a ``VagrantFile`` for setting up a sandbox VM where you can play around
with the functionality.  Bring up the Vagrant box::

    $ vagrant up

This may take a while but will set up a Ubuntu Precise64 VM with RabbitMQ
installed.  You can then SSH into the machine and run the Django
development server::

    $ vagrant ssh
    $ cd /vagrant/sandbox
    $ ./manage.py runserver 0.0.0.0:8000

The dummy site will be available at ``http://localhost:8080`` on your host
machine.  There are some sample views in ``sandbox/dummyapp/views.py`` that
exercise django-cacheback.

Run a Celery worker using::

    $ celery -A sandbox worker --loglevel=INFO
