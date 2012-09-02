===
API
===

The main class is ``cacheback.Job`` which provides several methods intended to
be overridden and customised:

.. autoclass:: cacheback.Job
    :members: fetch, expiry, should_item_by_fetched_synchronously, empty, key, prepare_args, prepare_kwargs


Queryset jobs
=============

There are two classes for easy caching of ORM reads.  These don't need
subclassing but rather take the model class as a ``__init__`` parameter.

.. autoclass:: cacheback.QuerySetFilterJob
    :members:

.. autoclass:: cacheback.QuerySetGetJob
    :members:

Example usage::
 
    from django.contrib.auth import models
    from django.shortcuts import render
    from cacheback import QuerySetGetJob, QuerySetFilterJob

    def user_detail(request, username):
        user = QuerySetGetJob(models.User).get(username=username)
        return render(request, 'user.html',
                      {'user': user})

    def staff(request):
        staff = QuerySetFilterJob(models.User).filter(is_staff=True)
        return render(request, 'staff.html',
                      {'users': staff})

These classes are helpful for simple ORM reads but won't be suitable for more
complicated queries where ``filter`` is chained together with ``exclude``.
