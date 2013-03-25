import time

from django.core.cache import cache
from django.test import TestCase
from django.test.utils import override_settings
import mock

from cacheback.base import Job



class StaleSyncJob(Job):
    # Cache items for 5 seconds.
    # -> trigger an async refresh if item is 5 < x < 10 seconds old
    # -> trigger a sync refresh if item is x > 10 seconds old
    lifetime = 5
    fetch_on_stale_threshold = 10

    def __init__(self):
        self.called_async = False

    def fetch(self):
        return 'testing'

    def async_refresh(self, *args, **kwargs):
        self.called_async = True
        super(StaleSyncJob, self).async_refresh(*args, **kwargs)


@override_settings(CELERY_ALWAYS_EAGER=False)
class TestJobWithStaleSyncRefreshAttributeSet(TestCase):

    def setUp(self):
        self.job = StaleSyncJob()
        # Populate cache
        self.cache_time = time.time()
        self.job.refresh()

    def tearDown(self):
        cache.clear()

    def test_hits_cache_within_cache_lifetime(self):
        self.assertEqual('testing', self.job.get())
        self.assertFalse(self.job.called_async)

    def test_triggers_async_refresh_after_lifetime_but_before_stale_threshold(self):
        with mock.patch('time.time') as mocktime:
            mocktime.return_value = self.cache_time + 7
            self.assertEqual('testing', self.job.get())
            self.assertTrue(self.job.called_async)

    def test_triggers_sync_refresh_after_stale_threshold(self):
        with mock.patch('time.time') as mocktime:
            mocktime.return_value = self.cache_time + 12
            self.assertEqual('testing', self.job.get())
            self.assertFalse(self.job.called_async)
