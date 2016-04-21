import logging

from django.conf import settings
from django.core import signals
from django.core.exceptions import ImproperlyConfigured


try:
    import importlib
except ImportError:
    import django.utils.importlib as importlib

try:
    from .tasks import refresh_cache as celery_refresh_cache
except ImportError:
    celery_refresh_cache = None

try:
    from .rq_tasks import refresh_cache as rq_refresh_cache
except ImportError as exc:
    rq_refresh_cache = None


logger = logging.getLogger('cacheback')


def get_cache(backend, **kwargs):
    """
    Compatibilty wrapper for getting Django's cache backend instance

    original source:
    https://github.com/vstoykov/django-imagekit/commit/c26f8a0538778969a64ee471ce99b25a04865a8e
    """
    try:
        from django.core.cache import _create_cache
    except ImportError:
        # Django < 1.7
        from django.core.cache import get_cache as _get_cache
        return _get_cache(backend, **kwargs)

    cache = _create_cache(backend, **kwargs)
    # Some caches -- python-memcached in particular -- need to do a cleanup at the
    # end of a request cycle. If not implemented in a particular backend
    # cache.close is a no-op. Not available in Django 1.5
    if hasattr(cache, 'close'):
        signals.request_finished.connect(cache.close)
    return cache


def get_job_class(klass_str):
    """
    Return the job class
    """
    mod_name, klass_name = klass_str.rsplit('.', 1)
    try:
        mod = importlib.import_module(mod_name)
    except ImportError as e:
        logger.error("Error importing job module %s: '%s'", mod_name, e)
        return
    try:
        klass = getattr(mod, klass_name)
    except AttributeError:
        logger.error("Module '%s' does not define a '%s' class", mod_name, klass_name)
        return
    return klass


def enqueue_task(*args, **kwargs):
    task_queue = getattr(settings, 'CACHEBACK_TASK_QUEUE', 'celery')

    if task_queue == 'rq' and rq_refresh_cache is not None:
        return rq_refresh_cache.delay(**kwargs['kwargs'])

    elif task_queue == 'celery' and celery_refresh_cache is not None:
        return celery_refresh_cache.apply_async(*args, **kwargs)

    raise ImproperlyConfigured('Unkown task queue configured: {0}'.format(task_queue))
