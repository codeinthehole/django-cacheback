import cacheback

from dummyapp import models


class VanillaJob(cacheback.AsyncCacheJob):
    fetch_on_miss = False

    def fetch(self):
        import time
        time.sleep(10)
        return models.DummyModel.objects.all()


class KeyedJob(cacheback.AsyncCacheJob):

    def key(self, name):
        return name

    def fetch(self, name):
        return models.DummyModel.objects.filter(name=name)