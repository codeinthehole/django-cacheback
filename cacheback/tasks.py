from celery import shared_task
from django.conf import settings


ignore_result = getattr(settings, 'CACHEBACK_CELERY_IGNORE_RESULT', False)


@shared_task(ignore_result=ignore_result)
def refresh_cache(klass_str, obj_args, obj_kwargs, call_args, call_kwargs):
    from .base import Job
    Job.perform_async_refresh(klass_str, obj_args, obj_kwargs, call_args, call_kwargs)
