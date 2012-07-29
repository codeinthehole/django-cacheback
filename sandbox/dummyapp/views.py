from django.shortcuts import render

from async_cache.jobs import QuerySetFilterJob
from dummyapp import jobs
from dummyapp import models


def index(request):
    if 'name' in request.GET:
        name = request.GET['name']
        if 'qs' in request.GET:
            items = QuerySetFilterJob(models.DummyModel).get(name=name)
        else:
            items = jobs.KeyedJob().get(name=request.GET['name'])
    else:
        items = jobs.VanillaJob().get()
    return render(request, 'index.html', {'items': items})
