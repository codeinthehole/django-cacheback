from celery import shared_task


@shared_task
def refresh_cache(klass_str, obj_args, obj_kwargs, call_args, call_kwargs):
    from .base import Job
    Job.perform_async_refresh(klass_str, obj_args, obj_kwargs, call_args, call_kwargs)
