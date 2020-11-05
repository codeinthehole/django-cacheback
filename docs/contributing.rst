============
Contributing
============

Make sure to have `poetry` installed. Then, start by cloning the repo,
and installing the dependencies:

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
