from django.shortcuts import render

from cacheback import QuerySetFilterJob, FunctionJob, cacheback
from dummyapp import jobs
from dummyapp import models

def fetch():
    return models.DummyModel.objects.filter(name__contains='1')

def fetch_with_arg(q):
    return models.DummyModel.objects.filter(name__contains=q)

@cacheback(5)
def decorated(q):
    return models.DummyModel.objects.filter(name__contains=q)

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
        if 'q' in request.GET:
            items = job.get(fetch_with_arg, request.GET['q'])
        else:
            items = job.get(fetch)
    if 'decorator' in request.GET:
        items = decorated('3')
    else:
        items = jobs.VanillaJob().get()
    return render(request, 'index.html', {'items': items})
