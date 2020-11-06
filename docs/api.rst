===
API
===

Jobs
====

The main class is ``cacheback.base.Job``.  The methods that are intended to be
called from client code are:

.. autoclass:: cacheback.base.Job
    :members: get, invalidate, delete

It has some class properties than can be used to configure simple behaviour:

.. autoclass:: cacheback.base.Job
    :noindex:
    :members: lifetime, refresh_timeout, cache_alias, fetch_on_miss, fetch_on_stale_threshold, task_options

There are also several methods intended to be overridden and customised:

.. autoclass:: cacheback.base.Job
    :noindex:
    :members: key, fetch, expiry, should_missing_item_be_fetched_synchronously, should_stale_item_be_fetched_synchronously, empty, key, prepare_args, prepare_kwargs, timeout, process_result


Queryset jobs
=============

There are two classes for easy caching of ORM reads.  These don't need
subclassing but rather take the model class as a ``__init__`` parameter.

.. autoclass:: cacheback.jobs.QuerySetFilterJob
    :members:

.. autoclass:: cacheback.jobs.QuerySetGetJob
    :members:


Example usage:

.. sourcecode:: python

    from django.contrib.auth import models
    from django.shortcuts import render
    from cacheback.jobs import QuerySetGetJob, QuerySetFilterJob

    def user_detail(request, username):
        user = QuerySetGetJob(models.User).get(username=username)
        return render(request, 'user.html', {'user': user})

    def staff(request):
        staff = QuerySetFilterJob(models.User).get(is_staff=True)
        return render(request, 'staff.html', {'users': staff})

These classes are helpful for simple ORM reads but won't be suitable for more
complicated queries where ``filter`` is chained together with ``exclude``.
