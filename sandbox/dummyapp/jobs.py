import cacheback

from dummyapp import models


class VanillaJob(cacheback.Job):
    fetch_on_miss = False

    def fetch(self):
        import time
        time.sleep(10)
        return models.DummyModel.objects.all()


class KeyedJob(cacheback.Job):

    def key(self, name):
        return name

    def fetch(self, name):
        return models.DummyModel.objects.filter(name=name)