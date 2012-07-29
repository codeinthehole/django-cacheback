import logging
import time

from celery import task
from django.utils import importlib


logger = logging.getLogger(__name__)


@task()
def refresh_cache(klass, *args, **kwargs):
    """
    Re-populate cache using the given job class and parameters to call the
    'refresh' method with.

    :klass: String repr of class (eg 'apps.twitter.jobs.FetchTweetsJob')
    :args: Function args
    :kwargs: Function kwargs
    """
    logger.info("Running %s with args %r and kwargs %r", klass, args,
                kwargs)
    mod_name, klass_name = klass.rsplit('.', 1)
    try:
        mod = importlib.import_module(mod_name)
    except ImportError,e :
        logger.error("Error importing job module %s: '%s'", mod_name, e)
        return
    try:
        klass = getattr(mod, klass_name)
    except AttributeError:
        logger.error("Module '%s' does not define a '%s' class", mod_name,
                     klass_name)
    start = time.time()
    try:
        klass().refresh(*args, **kwargs)
    except Exception, e:
        logger.error("Error running job: '%s'", e)
    else:
        duration = time.time() - start
        logger.info("Fetched data in %.6f seconds", duration)