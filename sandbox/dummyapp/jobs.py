import async_cache

from dummyapp import models


class VanillaJob(async_cache.AsyncCacheJob):
    fetch_on_empty = False

    def fetch(self):
        import time
        time.sleep(10)
        return models.DummyModel.objects.all()


class KeyedJob(async_cache.AsyncCacheJob):

    def key(self, name):
        return name

    def fetch(self, name):
        return models.DummyModel.objects.filter(name=name)