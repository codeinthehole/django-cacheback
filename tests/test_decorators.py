import pytest

from cacheback.decorators import cacheback
from cacheback.jobs import FunctionJob


class OtherFunctionJob(FunctionJob):
    pass


@cacheback(fetch_on_miss=False, job_class=OtherFunctionJob)
def no_fetch_miss_function(param):
    return 'JOB-EXECUTED:{0}'.format(param)


@cacheback(lifetime=30, fetch_on_miss=True)
def fetch_miss_function(param):
    return 'JOB-EXECUTED:{0}'.format(param)


@cacheback(cache_alias='secondary', fetch_on_miss=True)
def fetch_cache_alias_function(param):
    return 'JOB-EXECUTED:{0}'.format(param)


@cacheback(set_data_kwarg='my_data')
def custom_payload_label_function(param):
    return 'JOB-EXECUTED:{0}'.format(param)


@pytest.mark.usefixtures('cleared_cache', scope='function')
class TestCachebackDecorator:

    def test_job_init(self):
        assert isinstance(fetch_miss_function.job, FunctionJob)
        assert fetch_miss_function.job.lifetime == 30

        assert isinstance(fetch_cache_alias_function.job, FunctionJob)
        assert fetch_cache_alias_function.job.cache_alias == 'secondary'

    def test_job_init_job_class(self):
        assert isinstance(no_fetch_miss_function.job, OtherFunctionJob)

    @pytest.mark.redis_required
    def test_miss_no_fetch(self, rq_worker):
        assert no_fetch_miss_function('foo') is None
        assert len(rq_worker.queues[0].jobs) == 1

    def test_miss_fetch(self):
        assert fetch_miss_function('foo') == 'JOB-EXECUTED:foo'

    def test_cache_alias(self):
        assert fetch_cache_alias_function('foo') == 'JOB-EXECUTED:foo'

    def test_set(self):
        no_fetch_miss_function.job.set(
            no_fetch_miss_function, 'foo', 'MANUALLY_SET')

        assert no_fetch_miss_function('foo') == 'MANUALLY_SET'

    def test_set_kwarg(self):
        no_fetch_miss_function.job.set(
            no_fetch_miss_function, 'foo', data='MANUALLY_SET_WITH_KWARG')

        assert no_fetch_miss_function('foo') == 'MANUALLY_SET_WITH_KWARG'

    def test_set_custom_kwarg(self):
        custom_payload_label_function.job.set(
            custom_payload_label_function, 'foo', my_data='MANUALLY_SET_WITH_CUSTOM_KWARG')

        assert custom_payload_label_function('foo') == 'MANUALLY_SET_WITH_CUSTOM_KWARG'

    @pytest.mark.redis_required
    def test_hit(self, rq_burst):
        assert no_fetch_miss_function('foo') is None
        rq_burst()
        assert no_fetch_miss_function('foo') == 'JOB-EXECUTED:foo'
