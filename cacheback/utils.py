import importlib
import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


try:
    from .tasks import refresh_cache as celery_refresh_cache
except ImportError:
    celery_refresh_cache = None

try:
    import django_rq

    from .rq_tasks import refresh_cache as rq_refresh_cache
except ImportError:
    django_rq = None
    rq_refresh_cache = None


logger = logging.getLogger('cacheback')


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


def enqueue_task(kwargs, task_options=None):
    task_queue = getattr(settings, 'CACHEBACK_TASK_QUEUE', 'celery')

    if task_queue == 'rq' and rq_refresh_cache is not None:
        queue = django_rq.get_queue(**task_options or {})
        return queue.enqueue_call(
            rq_refresh_cache,
            kwargs=kwargs,
            result_ttl=0 if getattr(settings, 'CACHEBACK_TASK_IGNORE_RESULT', False) else None,
        )

    elif task_queue == 'celery' and celery_refresh_cache is not None:
        return celery_refresh_cache.apply_async(kwargs=kwargs, **task_options or {})

    raise ImproperlyConfigured(f'Unknown task queue or backend is not configured: {task_queue}')
