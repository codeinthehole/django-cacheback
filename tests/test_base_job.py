import mock
import pytest
from django.core.cache.backends.base import BaseCache
from django.utils import timezone
from freezegun import freeze_time

from cacheback.base import Job
from tests.dummyapp.models import DummyModel


class DummyJob(Job):

    def fetch(self, param):
        return ('JOB-EXECUTED:{0}'.format(param), timezone.now())


class EmptyDummyJob(DummyJob):
    fetch_on_miss = False


class StaleDummyJob(DummyJob):
    fetch_on_stale_threshold = 900


class FailJob(Job):

    def fetch(self):
        raise Exception('JOB-FAILED')


@pytest.mark.usefixtures('cleared_cache', scope='function')
class TestJob:

    def test_init(self):
        job = DummyJob()
        assert isinstance(job.cache, BaseCache)
        assert job.task_options == {}

    def test_get_miss_sync(self):
        assert DummyJob().get('foo')[0] == 'JOB-EXECUTED:foo'

    @pytest.mark.redis_required
    def test_get_miss_empty_async(self, rq_burst):
        job = EmptyDummyJob()
        assert job.get('foo') is None
        rq_burst()
        assert job.get('foo')[0] == 'JOB-EXECUTED:foo'

    def test_get_stale_sync(self):
        job = StaleDummyJob()
        with freeze_time('2016-03-20 14:00'):
            first_result = job.get('foo')

        with freeze_time('2016-03-20 14:16'):
            second_result = job.get('foo')

        assert first_result[1] < second_result[1]

    @pytest.mark.redis_required
    def test_get_stale_async(self, rq_burst):
        job = StaleDummyJob()
        with freeze_time('2016-03-20 14:00'):
            first_result = job.get('foo')

        with freeze_time('2016-03-20 14:14'):
            second_result = job.get('foo')

        assert first_result[1] == second_result[1]

        with freeze_time('2016-03-20 14:16'):
            rq_burst()

        with freeze_time('2016-03-20 14:17'):
            third_result = job.get('foo')

        assert second_result[1] < third_result[1]

    @pytest.mark.redis_required
    def test_get_hit(self, rq_worker):
        job = StaleDummyJob()
        with freeze_time('2016-03-20 14:00'):
            first_result = job.get('foo')

        with freeze_time('2016-03-20 14:05'):
            second_result = job.get('foo')

        assert first_result[1] == second_result[1]

        # Check if a task was inserted.
        assert len(rq_worker.queues[0].jobs) == 0

    @pytest.mark.redis_required
    def test_invalidate_miss(self, rq_worker):
        DummyJob().invalidate('foo')
        # There was no cached item, nothing todo.
        assert len(rq_worker.queues[0].jobs) == 0

    @pytest.mark.redis_required
    def test_invalidate_hit(self, rq_worker):
        job = DummyJob()
        job.refresh('foo')
        job.invalidate('foo')
        assert len(rq_worker.queues[0].jobs) == 1

    def test_delete_miss(self):
        job = DummyJob()
        job.delete('foo')
        assert job.key('foo') not in job.cache

    def test_delete_hit(self):
        job = DummyJob()
        job.refresh('foo')
        assert job.key('foo') in job.cache
        job.delete('foo')
        assert job.key('foo') not in job.cache

    def test_store(self):
        job = DummyJob()
        job.cache_set(job.key('foo'), job.expiry(), True)
        assert job.key('foo') in job.cache

    def test_store_verify_fail(self, settings):
        settings.CACHES = {
            'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}
        settings.CACHEBACK_VERIFY_CACHE_WRITE = True
        job = DummyJob()

        with pytest.raises(RuntimeError) as exc:
            job.cache_set(job.key('foo'), job.expiry(), True)

        assert 'Unable to save' in str(exc.value)

    def test_store_no_verify_fail(self, settings):
        settings.CACHES = {
            'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}
        settings.CACHEBACK_VERIFY_CACHE_WRITE = False
        job = DummyJob()
        job.cache_set(job.key('foo'), job.expiry(), True)
        assert job.key('foo') not in job.cache

    def test_refresh(self):
        job = DummyJob()
        result = job.refresh('foo')
        assert result[0] == 'JOB-EXECUTED:foo'
        assert job.key('foo') in job.cache

    @pytest.mark.redis_required
    def test_async_refresh(self, rq_worker):
        job = DummyJob()
        job.async_refresh('foo')
        assert job.key('foo') not in job.cache
        assert len(rq_worker.queues[0].jobs) == 1

    @mock.patch('cacheback.base.enqueue_task')
    def test_async_refresh_task_fail(self, enqueue_mock):
        enqueue_mock.side_effect = Exception
        job = DummyJob()
        job.async_refresh('foo')
        assert job.get('foo')[0] == 'JOB-EXECUTED:foo'

    @mock.patch('cacheback.base.enqueue_task')
    @mock.patch('cacheback.base.Job.refresh')
    def test_async_refresh_task_fail_sync_fail(self, refresh_mock, enqueue_mock):
        refresh_mock.side_effect = Exception
        enqueue_mock.side_effect = Exception
        job = DummyJob()
        job.async_refresh('foo')
        assert job.key('foo') not in job.cache

    def test_expiry(self):
        with freeze_time('2016-03-20 14:05'):
            job = DummyJob()
            assert job.expiry() == 1458483300

    def test_timeout(self):
        with freeze_time('2016-03-20 14:05'):
            job = DummyJob()
            assert job.timeout() == 1458482760

    def test_should_stale_item_be_fetched_synchronously_no_threshold(self):
        assert DummyJob().should_stale_item_be_fetched_synchronously(0) is False

    def test_should_stale_item_be_fetched_synchronously_reached(self):
        assert StaleDummyJob().should_stale_item_be_fetched_synchronously(301) is True

    def test_should_stale_item_be_fetched_synchronously_not_reached(self):
        assert StaleDummyJob().should_stale_item_be_fetched_synchronously(300) is False

    def test_key_no_args_no_kwargs(self):
        assert DummyJob().key() == 'tests.test_base_job.DummyJob'

    def test_key_args_no_kwargs(self):
        assert DummyJob().key(1, 2, 3) == (
            'tests.test_base_job.DummyJob:7b6e2994f12a7e000c01190edec1921e')

    def test_key_no_args_kwargs(self):
        assert DummyJob().key(foo='bar') == (
            'tests.test_base_job.DummyJob:d41d8cd98f00b204e9800998ecf8427e:'
            'acbd18db4cc2f85cedef654fccc4a4d8:37b51d194a7513e45b56f6524f2d51f2'
        )

    def test_key_args_kwargs(self):
        assert DummyJob().key(1, 2, foo='bar', bar='baz') == (
            'tests.test_base_job.DummyJob:def474a313bffa002eae8941b2e12620:'
            '8856328b99ee7881e9bf7205296e056d:c9ebc77141c29f6d619cf8498631343d'
        )

    @pytest.mark.django_db
    def test_key_django_model(self):
        alan = DummyModel.objects.create(name="Alan")
        john = DummyModel.objects.create(name="John")
        assert DummyJob().key(alan) == \
            'tests.test_base_job.DummyJob:9df82067f944cc95795bc89ec0aa65df'
        assert DummyJob().key(alan) != DummyJob().key(john)

    @mock.patch('cacheback.base.logger')
    def test_job_refresh_unkown_jobclass(self, logger_mock):
        Job.job_refresh('foomodule.BarJob', (), {}, (), {})
        assert 'Unable to construct %s with' in (logger_mock.error.call_args[0][0])
        assert logger_mock.error.call_args[0][1] == 'foomodule.BarJob'

    @mock.patch('cacheback.base.logger')
    def test_job_refresh_perform_error(self, logger_mock):
        Job.job_refresh('tests.test_base_job.FailJob', (), {}, (), {})
        assert 'Error running job' in (logger_mock.exception.call_args[0][0])
        assert isinstance(logger_mock.exception.call_args[0][1], Exception)

    def test_job_refresh(self):
        Job.job_refresh('tests.test_base_job.EmptyDummyJob', (), {}, ('foo',), {})
        assert EmptyDummyJob().get('foo') is not None
