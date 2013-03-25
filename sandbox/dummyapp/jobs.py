from cacheback.base import Job

from dummyapp import models


class VanillaJob(Job):
    fetch_on_miss = False
    refresh_timeout = 5

    def fetch(self):
        import time
        time.sleep(10)
        return models.DummyModel.objects.all()


class KeyedJob(Job):
    lifetime = 5
    fetch_on_stale_threshold = 10

    def key(self, name):
        return name

    def fetch(self, name):
        return models.DummyModel.objects.filter(name=name)
