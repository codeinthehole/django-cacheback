import django_rq
import pytest
import redis
from django.conf import settings
from django.core.cache import cache


def skip_if_no_redis():
    if not hasattr(skip_if_no_redis, '_test_result'):
        try:
            redis.StrictRedis(
                settings.RQ_QUEUES['default'].get('HOST', 'localhost'),
                settings.RQ_QUEUES['default'].get('POST', 6379)
            ).ping()
            skip_if_no_redis._redis_available = True
        except redis.ConnectionError:
            skip_if_no_redis._redis_available = False

    if not skip_if_no_redis._redis_available:
        pytest.skip('Redis server not available.')


def pytest_runtest_setup(item):
    if item.get_marker('redis_required'):
        skip_if_no_redis()


@pytest.fixture(scope='session', autouse=True)
def session_clear_cache(request):
    cache.clear()
    request.addfinalizer(lambda: cache.clear())


@pytest.fixture()
def cleared_cache(request):
    cache.clear()


@pytest.yield_fixture
def rq_worker(request):
    [queue.empty() for queue in django_rq.get_worker().queues]

    worker = django_rq.get_worker()

    yield worker

    [queue.empty() for queue in django_rq.get_worker().queues]


@pytest.yield_fixture
def rq_burst(request, rq_worker):

    def burst():
        rq_worker.work(burst=True)

    yield burst
