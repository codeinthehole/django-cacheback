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

Alternatively, there's a ``docker compose`` stack for setting up a sandbox
environment where you can play around with the functionality.
Bring up the compose stack::

    $ docker compose up

The stack will start with Celery as a broker by default. You can Alternatively
make use of rq by supplying the `Q` env var:

    $ Q=rq docker compose up

The above commands will start a Django runserver and the selected task worker.
The dummy site will be available at ``http://localhost:8080`` on your host
machine.  There are some sample views in ``sandbox/dummyapp/views.py`` that
exercise django-cacheback.
