from django.test import TestCase
from django.core.cache import cache
from django.db import connection

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

    def test_only_one_database_query(self):
        with self.assertNumQueries(1):
            for _ in xrange(10):
                self.job.get('Alan')
