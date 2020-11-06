from django.urls import path

from dummyapp import views


urlpatterns = [
    path('', views.index, name='index'),
]
