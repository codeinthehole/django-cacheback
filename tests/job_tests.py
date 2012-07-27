from django.test import TestCase
from django.core.cache import cache

from async_cache import AsyncCacheJob
from tests.dummyapp import models


class UppercaseJob(AsyncCacheJob):

    def key(self, name):
        return name

    def fetch(self, name):
        return name.upper()


class QuerySetJob(AsyncCacheJob):

    def key(self, name):
        return name

    def fetch(self, name):
        return models.DummyModel.objects.filter(name=name)


class TestUppercaseJob(TestCase):

    def setUp(self):
        self.job = UppercaseJob()

    def tearDown(self):
        cache.clear()

    def test_first_pass_returns_none(self):
        self.assertIsNone(self.job.get('dave'))

    def test_second_pass_returns_value(self):
        self.assertIsNone(self.job.get('dave'))
        self.assertEqual('DAVE', self.job.get('dave'))


class TestQuerySetJob(TestCase):

    def setUp(self):
        self.job = QuerySetJob()
        models.DummyModel.objects.create(name="Alan")
        models.DummyModel.objects.create(name="Barry")

    def tearDown(self):
        models.DummyModel.objects.all().delete()
        cache.clear()

    def test_first_pass_returns_none(self):
        self.assertIsNone(self.job.get('Alan'))

    def test_second_pass_returns_queryset(self):
        self.assertIsNone(self.job.get('Alan'))
        self.assertEqual(1, len(self.job.get('Alan')))
