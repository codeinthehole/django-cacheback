============
Installation
============

You need to do four things:

1. Install Cacheback
~~~~~~~~~~~~~~~~~~~~

Run::

    pip install django-cacheback

and add ``cacheback`` to your ``INSTALLED_APPS``.  

2. Add djcelery
~~~~~~~~~~~~~~~

The 'django-celery' package will be installed by pip as part of step 1, but you
will also need to complete the `djcelery installation process`_ by adding ``djcelery`` to
your ``INSTALLED_APPS`` and including::

    import djcelery
    dlcelery.setup_loader()

.. _`djcelery installation process`: http://pypi.python.org/pypi/django-celery/3.0.9

in your settings.  

3. Install a message broker
~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
Celery requires a message broker.  Use `Celery's tutorial`_ to help set one up.
I recommend rabbitmq.

.. _`Celery's tutorial`: http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html

4. Set up a cache
~~~~~~~~~~~~~~~~~

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
-------

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

