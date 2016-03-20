import pytest

from cacheback.decorators import cacheback
from cacheback.function import FunctionJob


class OtherFunctionJob(FunctionJob):
    pass


@cacheback(fetch_on_miss=False, job_class=OtherFunctionJob)
def no_fetch_miss_function(param):
    return 'JOB-EXECUTED:{0}'.format(param)


@cacheback(lifetime=30, fetch_on_miss=True)
def fetch_miss_function(param):
    return 'JOB-EXECUTED:{0}'.format(param)


@pytest.mark.usefixtures('cleared_cache', scope='function')
class TestCachebackDecorator:

    def test_job_init(self):
        assert isinstance(fetch_miss_function.job, FunctionJob)
        assert fetch_miss_function.job.lifetime == 30

    def test_job_init_job_class(self):
        assert isinstance(no_fetch_miss_function.job, OtherFunctionJob)

    @pytest.mark.redis_required
    def test_miss_no_fetch(self, rq_worker):
        assert no_fetch_miss_function('foo') is None
        assert len(rq_worker.queues[0].jobs) == 1

    def test_miss_fetch(self):
        assert fetch_miss_function('foo') == 'JOB-EXECUTED:foo'

    @pytest.mark.redis_required
    def test_hit(self, rq_burst):
        assert no_fetch_miss_function('foo') is None
        rq_burst()
        assert no_fetch_miss_function('foo') == 'JOB-EXECUTED:foo'
