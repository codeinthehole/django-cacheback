from django.shortcuts import render

from cacheback import QuerySetFilterJob, FunctionJob
from dummyapp import jobs
from dummyapp import models

def fetch():
    return models.DummyModel.objects.filter(name__contains='1')

def index(request):
    if 'name' in request.GET:
        name = request.GET['name']
        if 'qs' in request.GET:
            items = QuerySetFilterJob(models.DummyModel).get(name=name)
        else:
            items = jobs.KeyedJob().get(name=request.GET['name'])
    if 'function' in request.GET:
        job = FunctionJob()
        job.fetch_on_empty = False
        items = job.get(fetch)
    else:
        items = jobs.VanillaJob().get()
    return render(request, 'index.html', {'items': items})
