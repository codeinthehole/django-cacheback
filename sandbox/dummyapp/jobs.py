from async_cache import jobs

from dummyapp import models


class VanillaJob(jobs.AsyncCacheJob):
    fetch_on_empty = False

    def fetch(self):
        import time
        time.sleep(10)
        return models.DummyModel.objects.all()


class KeyedJob(jobs.AsyncCacheJob):

    def key(self, name):
        return name

    def fetch(self, name):
        return models.DummyModel.objects.filter(name=name)