import uuid

import celery
import pytest

from cacheback.decorators import cacheback
from cacheback.jobs import FunctionJob, QuerySetFilterJob, QuerySetGetJob, QuerySetJob
from tests.dummyapp.models import DummyModel


def dummy_function(param):
    return 'JOB-EXECUTED:{0}'.format(param)


@cacheback()
def decorated_dummy_function(param):
    return 'JOB-EXECUTED:{0}'.format(param)


@pytest.mark.usefixtures('cleared_cache', scope='function')
class TestFunctionJob:
    def test_init_defaults(self):
        job = FunctionJob()
        assert job.lifetime == 600
        assert job.fetch_on_miss
        assert job.cache_alias == 'default'
        assert job.task_options == {}

    def test_init(self):
        job = FunctionJob(
            lifetime=30,
            fetch_on_miss=False,
            cache_alias='secondary',
            task_options={'foo': 'bar'},
        )
        assert job.lifetime == 30
        assert not job.fetch_on_miss
        assert job.cache_alias == 'secondary'
        assert job.task_options == {'foo': 'bar'}

    def test_prepare_args(self):
        job = FunctionJob()
        assert job.prepare_args(dummy_function, 'foo') == (
            'tests.test_jobs:dummy_function',
            'foo',
        )

    def test_fetch(self):
        assert FunctionJob().fetch('tests.test_jobs:dummy_function', 'foo') == (
            'JOB-EXECUTED:foo'
        )

    def test_fetch_decorated(self):
        assert FunctionJob().fetch('tests.test_jobs:decorated_dummy_function', 'foo') == (
            'JOB-EXECUTED:foo'
        )

    def test_init_kwargs(self):
        assert FunctionJob().get_init_kwargs() == {'lifetime': 600, 'cache_alias': 'default'}
        assert FunctionJob(lifetime=30).get_init_kwargs() == {
            'lifetime': 30,
            'cache_alias': 'default',
        }
        assert FunctionJob(cache_alias='secondary').get_init_kwargs() == {
            'lifetime': 600,
            'cache_alias': 'secondary',
        }

    def test_non_serializable_creates_one_entry(self, settings):
        settings.CELERY_TASK_ALWAYS_EAGER = True
        settings.CACHEBACK_TASK_QUEUE = "celery"

        dec_function = cacheback(fetch_on_miss=False)(dummy_function)

        arg = [uuid.uuid4()]
        str_arg = [str(x) for x in arg]

        sync_key = dec_function.job.key("tests.test_jobs:dummy_function", arg)
        async_key = dec_function.job.key("tests.test_jobs:dummy_function", str_arg)

        assert sync_key != async_key

        empty_result = dec_function(arg)

        assert empty_result is None
        assert dec_function.job.cache.has_key(sync_key)
        assert not dec_function.job.cache.has_key(async_key)

        result = dec_function(arg)

        # use str_arg for dummy_function as celery serializes the UUID as a str
        assert result == dummy_function(str_arg)

@pytest.mark.django_db
class TestQuerySetJob:
    def test_init_defaults(self):
        job = QuerySetJob(DummyModel)
        assert job.lifetime == 600
        assert job.fetch_on_miss
        assert job.cache_alias == 'default'
        assert job.task_options == {}

    def test_init(self):
        job = QuerySetJob(
            DummyModel,
            lifetime=30,
            fetch_on_miss=False,
            cache_alias='secondary',
            task_options={'foo': 'bar'},
        )
        assert job.lifetime == 30
        assert not job.fetch_on_miss
        assert job.cache_alias == 'secondary'
        assert job.task_options == {'foo': 'bar'}

    def test_key(self):
        assert QuerySetJob(DummyModel).key('foo') == (
            'DummyModel-cacheback.jobs.QuerySetJob:acbd18db4cc2f85cedef654fccc4a4d8'
        )

    def test_init_kwargs(self):
        assert QuerySetJob(DummyModel).get_init_kwargs() == {
            'model': DummyModel,
            'lifetime': 600,
            'cache_alias': 'default',
        }
        assert QuerySetJob(DummyModel, lifetime=30).get_init_kwargs() == {
            'model': DummyModel,
            'lifetime': 30,
            'cache_alias': 'default',
        }
        assert QuerySetJob(DummyModel, cache_alias='secondary').get_init_kwargs() == {
            'model': DummyModel,
            'lifetime': 600,
            'cache_alias': 'secondary',
        }


@pytest.mark.django_db
class TestQuerySetGetJob:
    def test_fetch(self):
        dummy1 = DummyModel.objects.create(name='Foo')
        assert QuerySetGetJob(DummyModel).fetch(name='Foo') == dummy1


@pytest.mark.django_db
class TestQuerySetGetFilterJob:
    def test_fetch(self):
        dummy1 = DummyModel.objects.create(name='Foo')
        dummy2 = DummyModel.objects.create(name='Bar')
        dummy3 = DummyModel.objects.create(name='Foobar')

        qset = list(QuerySetFilterJob(DummyModel).fetch(name__startswith='Foo'))
        assert dummy1 in qset
        assert dummy2 not in qset
        assert dummy3 in qset
