from django.conf.urls import patterns, url

from dummyapp import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
