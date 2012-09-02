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
