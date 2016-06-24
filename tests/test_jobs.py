import pytest

from cacheback.decorators import cacheback
from cacheback.function import FunctionJob
from cacheback.queryset import QuerySetFilterJob, QuerySetGetJob, QuerySetJob
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
        assert job.fetch_on_miss is True
        assert job.task_options == {}

    def test_init(self):
        job = FunctionJob(lifetime=30, fetch_on_miss=False, task_options={'foo': 'bar'})
        assert job.lifetime == 30
        assert job.fetch_on_miss is False
        assert job.task_options == {'foo': 'bar'}

    def test_prepare_args(self):
        job = FunctionJob()
        assert job.prepare_args(dummy_function, 'foo') == (
            'tests.test_jobs:dummy_function', 'foo')

    def test_fetch(self):
        assert FunctionJob().fetch('tests.test_jobs:dummy_function', 'foo') == (
            'JOB-EXECUTED:foo')

    def test_fetch_decorated(self):
        assert FunctionJob().fetch('tests.test_jobs:decorated_dummy_function', 'foo') == (
            'JOB-EXECUTED:foo')

    def test_init_kwargs(self):
        assert FunctionJob().get_constructor_kwargs() == {
            'lifetime': 600}
        assert FunctionJob(lifetime=30).get_constructor_kwargs() == {
            'lifetime': 30}


@pytest.mark.django_db
class TestQuerySetJob:

    def test_init_defaults(self):
        job = QuerySetJob(DummyModel)
        assert job.lifetime == 600
        assert job.fetch_on_miss is True
        assert job.task_options == {}

    def test_init(self):
        job = QuerySetJob(
            DummyModel, lifetime=30, fetch_on_miss=False, task_options={'foo': 'bar'})
        assert job.lifetime == 30
        assert job.fetch_on_miss is False
        assert job.task_options == {'foo': 'bar'}

    def test_key(self):
        assert QuerySetJob(DummyModel).key('foo') == (
            'DummyModel-cacheback.queryset.QuerySetJob:acbd18db4cc2f85cedef654fccc4a4d8')

    def test_init_kwargs(self):
        assert QuerySetJob(DummyModel).get_constructor_kwargs() == {
            'model': DummyModel, 'lifetime': 600}
        assert QuerySetJob(DummyModel, lifetime=30).get_constructor_kwargs() == {
            'model': DummyModel, 'lifetime': 30}


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
