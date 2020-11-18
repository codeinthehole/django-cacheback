============
Contributing
============

Make sure to have `poetry` installed. Then, start by cloning the repo,
and installing the dependencies::

    $ pip install poetry  # if not already installed
    $ cd <repository directory>
    $ poetry install


Running tests
=============

Use::

    # only runs actual tests
    $ make pytests

or::

    # runs tests but also linters like black, isort and flake8
    $ make tests


To generate html coverage::

    $ make coverage-html


Finally, you can also use tox to run tests against
all supported Django and Python versions::

    $ tox


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
