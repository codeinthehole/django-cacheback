============
Contributing
============

Get set up by cloning, creating a virtualenv and running::

    make develop

to install the testing dependencies.

Running tests
=============

Use::

    ./runtests.py

Sandbox VM
==========

There is a VagrantFile for setting up a sandbox VM where you can play around
with the functionality.  Bring up the Vagrant box::

    vagrant up

then provision:

    cd /vagrant/sandbox
    ./provision.sh

This may take a while but will set up a Ubuntu Precise64 VM with RabbitMQ
installed and configured.  You can then SSH into the machine and run the Django
development server::

    vagrant ssh
    cd /vagrant/sandbox
    ./manage.py loaddata/fixture.json
    ./manage.py runserver 0.0.0.0:8000

The dummy site will be available at ``localhost:8080``.  There are some sample
views in ``sandbox/dummyapp/views.py`` that exercise django-cacheback.

Run a Celery worker using::

    ./manage.py celery worker --loglevel=INFO
