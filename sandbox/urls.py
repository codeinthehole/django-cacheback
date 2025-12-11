from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls

from dummyapp import views


urlpatterns = [
    path('', views.index, name='index'),
] + debug_toolbar_urls()
