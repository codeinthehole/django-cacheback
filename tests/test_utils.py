import mock
import pytest
from django.core.exceptions import ImproperlyConfigured

from cacheback.utils import enqueue_task, get_job_class


class DummyClass:
    pass


class TestGetJobClass:

    @mock.patch('cacheback.utils.logger')
    def test_invalid_module(self, logger_mock):
        assert get_job_class('tests.foo.DummyClass') is None
        assert 'Error importing job module' in logger_mock.error.call_args[0][0]
        assert logger_mock.error.call_args[0][1] == 'tests.foo'

    @mock.patch('cacheback.utils.logger')
    def test_invalid_class(self, logger_mock):
        assert get_job_class('tests.test_utils.OtherDummyClass') is None
        assert 'define a \'%s\' class' in logger_mock.error.call_args[0][0]
        assert logger_mock.error.call_args[0][1] == 'tests.test_utils'
        assert logger_mock.error.call_args[0][2] == 'OtherDummyClass'

    def test_class(self):
        assert get_job_class('tests.test_utils.DummyClass') == DummyClass


class TestEnqueueTask:

    @mock.patch('cacheback.utils.rq_refresh_cache')
    @mock.patch('cacheback.utils.celery_refresh_cache')
    def test_celery(self, celery_mock, rq_mock, settings):
        settings.CACHEBACK_TASK_QUEUE = 'celery'
        enqueue_task({'bar': 'baz'}, task_options={'foo': 'bar'})
        assert celery_mock.apply_async.called is True
        assert celery_mock.apply_async.call_args[1] == {
            'kwargs': {'bar': 'baz'}, 'foo': 'bar'}
        assert rq_mock.delay.called is False

    @mock.patch('django_rq.get_queue')
    @mock.patch('cacheback.utils.celery_refresh_cache')
    def test_rq(self, celery_mock, rq_mock, settings):
        settings.CACHEBACK_TASK_QUEUE = 'rq'
        enqueue_task({'bar': 'baz'}, task_options={'foo': 'bar'})
        assert celery_mock.apply_async.called is False
        assert rq_mock.called is True
        assert rq_mock.call_args[1] == {'foo': 'bar'}
        assert rq_mock.return_value.enqueue_call.called is True
        assert rq_mock.return_value.enqueue_call.call_args[1] == {
            'kwargs': {'bar': 'baz'},
            'result_ttl': None
        }

    @mock.patch('django_rq.get_queue')
    @mock.patch('cacheback.utils.celery_refresh_cache')
    def test_rq_dont_store_result(self, celery_mock, rq_mock, settings):
        settings.CACHEBACK_TASK_QUEUE = 'rq'
        settings.CACHEBACK_TASK_IGNORE_RESULT = True
        enqueue_task({'bar': 'baz'}, task_options={'foo': 'bar'})
        assert celery_mock.apply_async.called is False
        assert rq_mock.called is True
        assert rq_mock.call_args[1] == {'foo': 'bar'}
        assert rq_mock.return_value.enqueue_call.called is True
        assert rq_mock.return_value.enqueue_call.call_args[1] == {
            'kwargs': {'bar': 'baz'},
            'result_ttl': 0
        }

    def test_unkown(self, settings):
        settings.CACHEBACK_TASK_QUEUE = 'unknown'
        with pytest.raises(ImproperlyConfigured) as exc:
            enqueue_task('foo')

        assert 'Unkown task queue' in str(exc.value)
