from django.shortcuts import render

from dummyapp import jobs


def index(request):
    if 'name' in request.GET:
        items = jobs.KeyedJob().get(name=request.GET['name'])
    else:
        items = jobs.VanillaJob().get()
    return render(request, 'index.html', {'items': items})
