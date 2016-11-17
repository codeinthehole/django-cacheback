import pytest
from django.core.cache import cache, caches
from django.core.cache.backends.dummy import DummyCache
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import six

import cacheback.base
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

    @pytest.mark.xfail
    def test_returns_result_on_second_call(self):
        self.assertIsNone(self.job.get())
        self.assertEqual((1, 2, 3), self.job.get())


class NoArgsSecondaryCacheJob(NoArgsJob):
    cache_alias = 'secondary'


class TestJobWithCacheAliasCalledWithNoArgs(TestCase):

    def setUp(self):
        self.job = NoArgsSecondaryCacheJob()

    def tearDown(self):
        caches['secondary'].clear()

    def test_returns_result_from_correct_cache(self):
        self.assertEqual((1, 2, 3), self.job.get())

        key = self.job.key()
        self.assertNotIn(key, cache)
        self.assertIn(key, caches['secondary'])


class SingleArgJob(Job):

    def fetch(self, name):
        return name.upper()


class AnotherSingleArgJob(Job):

    def fetch(self, name):
        return '%s!' % name.upper()


class TestSingleArgJob(TestCase):

    def setUp(self):
        self.job = SingleArgJob()

    def tearDown(self):
        cache.clear()

    def test_returns_correct_result(self):
        self.assertEqual('ALAN', self.job.get('alan'))
        self.assertEqual('BARRY', self.job.get('barry'))

    def test_jobs_with_duplicate_args_dont_clash_on_cache_key(self):
        another_job = AnotherSingleArgJob()
        self.assertEqual('ALAN', self.job.get('alan'))
        self.assertEqual('ALAN!', another_job.get('alan'))


class IntegerJob(Job):

    def fetch(self, obj):
        return 1


class TestNonIterableCacheItem(TestCase):

    def setUp(self):
        self.job = IntegerJob()
        self.job.fetch_on_miss = False

    def tearDown(self):
        cache.clear()

    @pytest.mark.xfail
    def test_returns_correct_result(self):
        self.assertIsNone(self.job.get(None))
        self.assertEqual(1, self.job.get(None))


class TestDummyCache(TestCase):

    def setUp(self):
        # Monkey-patch in the dummy cache
        self.cache = cache
        cacheback.base.cache = DummyCache('unique-snowflake', {})
        self.job = SingleArgJob()

    def tearDown(self):
        cacheback.base.cache = self.cache

    @override_settings(CACHEBACK_VERIFY_CACHE_WRITE=False)
    def test_dummy_cache_does_not_raise_error(self):
        self.assertEqual('ALAN', self.job.get('alan'))
        self.assertEqual('BARRY', self.job.get('barry'))


class EncodingJob(Job):

    def fetch(self, spam):
        return spam


class TestCacheKeyWithDifferentEncoding(TestCase):

    def setUp(self):
        self.job = EncodingJob()

    def test_unicode_and_bytestring_args(self):
        self.assertEqual(self.job.key(six.b('eggs')),
                         self.job.key(six.u('eggs')))

    def test_unicode_and_bytestring_kwargs(self):
        self.assertEqual(self.job.key(spam=six.b('eggs')),
                         self.job.key(spam=six.u('eggs')))
