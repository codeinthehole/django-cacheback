from django.test import TestCase
import cacheback.base
from django.core.cache.backends.dummy import DummyCache
from django.core.cache import cache


from cacheback.base import Job


class NoArgsJob(Job):
    def fetch(self):
        return 1, 2, 3


class TestDefaultJobCalledWithNoArgs(TestCase):

    def setUp(self):
        self.job = NoArgsJob()

    def tearDown(self):
        cache.clear()

    def test_returns_result_on_first_call(self):
        self.assertEqual((1, 2, 3), self.job.get())


class NoArgsUseEmptyJob(NoArgsJob):
    fetch_on_miss = False


class TestJobWithFetchOnMissCalledWithNoArgs(TestCase):
    """Test job with fetch_on_miss=False called with no args"""

    def setUp(self):
        self.job = NoArgsUseEmptyJob()

    def tearDown(self):
        cache.clear()

    def test_returns_none_on_first_call(self):
        self.assertIsNone(self.job.get())

    def test_returns_result_on_second_call(self):
        self.assertIsNone(self.job.get())
        self.assertEqual((1, 2, 3), self.job.get())


class SingleArgJob(Job):

    def fetch(self, name):
        return name.upper()


class TestSingleArgJob(TestCase):

    def setUp(self):
        self.job = SingleArgJob()

    def tearDown(self):
        cache.clear()

    def test_returns_correct_result(self):
        self.assertEqual('ALAN', self.job.get('alan'))
        self.assertEqual('BARRY', self.job.get('barry'))


class IntegerJob(Job):

    def fetch(self, obj):
        return 1


class TestNonIterableCacheItem(TestCase):

    def setUp(self):
        self.job = IntegerJob()
        self.job.fetch_on_miss = False

    def tearDown(self):
        cache.clear()

    def test_returns_correct_result(self):
        self.assertIsNone(self.job.get(None))
        self.assertEqual(1, self.job.get(None))


class DummyCacheTest(TestCase):

    def setUp(self):
        self.cache = cache
        cacheback.base.cache = DummyCache('unique-snowflake', {})
        self.job = SingleArgJob()

    def tearDown(self):
        cacheback.base.cache  = self.cache
    
    def test_dummy_cache_does_not_raise_error(self):
        self.assertEqual('ALAN', self.job.get('alan'))
        self.assertEqual('BARRY', self.job.get('barry'))
