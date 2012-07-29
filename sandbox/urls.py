from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'dummyapp.views.index', name='index'),
)
