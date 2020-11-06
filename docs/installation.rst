============
Installation
============

You need to do three things:

Install django-cacheback
~~~~~~~~~~~~~~~~~~~~~~~~

To install with Celery support, run::

    $ pip install django-cacheback[celery]

If you want to install with RQ support, just use::

    $ pip install django-cacheback[rq]

After installing the package and dependencies, add ``cacheback`` to your ``INSTALLED_APPS``.
If you want to use RQ as your task queue, you need to set ``CACHEBACK_TASK_QUEUE``
in your settings to ``rq``.

Install a message broker
~~~~~~~~~~~~~~~~~~~~~~~~

Celery requires a message broker.  Use `Celery's tutorial`_ to help set one up.
I recommend rabbitmq.


For RQ you need to set up a redis-server and configure ``django-rq``. Please look
up the `django-rq installation guide`_ for more details.

.. _`Celery's tutorial`: http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html
.. _`django-rq installation guide`: https://github.com/ui/django-rq#installation

Set up a cache
~~~~~~~~~~~~~~

You also need to ensure you have `a cache set up`_.  Most likely, you'll be using
memcache so your settings will include something like::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }

.. _`a cache set up`: https://docs.djangoproject.com/en/dev/topics/cache/?from=olddocs

Logging
~~~~~~~

You may also want to configure logging handlers for the 'cacheback' named
logger.  To set up console logging, use something like::

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            }
        },
        'loggers': {
            'cacheback': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }

