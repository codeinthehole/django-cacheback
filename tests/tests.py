from django.test import TestCase
from django.core.cache import cache

from async_cache import AsyncCacheJob


class UppercaseJob(AsyncCacheJob):

    def key(self, name):
        return name

    def fetch(self, name):
        return name.upper()


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
