from async_cache import jobs

from dummyapp import models


class VanillaJob(jobs.AsyncCacheJob):

    def fetch(self):
        return models.DummyModel.objects.all()


class KeyedJob(jobs.AsyncCacheJob):

    def key(self, name):
        return name

    def fetch(self, name):
        return models.DummyModel.objects.filter(name=name)