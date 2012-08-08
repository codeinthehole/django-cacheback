from django.test import TestCase
from django.core.cache import cache

from cacheback import Job, QuerySetFilterJob, QuerySetGetJob
from tests.dummyapp import models


class NoArgsJob(Job):
    def fetch(self):
        return 1,2,3


class TestNoArgsJob(TestCase):

    def setUp(self):
        self.job = NoArgsJob()

    def tearDown(self):
        cache.clear()

    def test_returns_result_on_first_call(self):
        self.assertEqual((1,2,3), self.job.get())


class NoArgsUseEmptyJob(NoArgsJob):
    fetch_on_miss = False


class TestNoArgsUseEmptyJob(TestCase):

    def setUp(self):
        self.job = NoArgsUseEmptyJob()

    def tearDown(self):
        cache.clear()

    def test_returns_none_on_first_call(self):
        self.assertIsNone(self.job.get())

    def test_returns_value_on_second_call(self):
        self.assertIsNone(self.job.get())
        self.assertEqual((1,2,3), self.job.get())


class SingleArgJob(Job):

    def fetch(self, name):
        return name.upper()


class TestSingleArgJob(TestCase):

    def setUp(self):
        self.job = SingleArgJob()

    def tearDown(self):
        cache.clear()

    def test_correct_results_returned(self):
        self.assertEqual('ALAN', self.job.get('alan'))
        self.assertEqual('BARRY', self.job.get('barry'))


class ManualQuerySetJob(Job):

    def fetch(self, name):
        return models.DummyModel.objects.filter(name=name)


class TestManualQuerySetJob(TestCase):

    def setUp(self):
        self.job = ManualQuerySetJob()
        models.DummyModel.objects.create(name="Alan")
        models.DummyModel.objects.create(name="Barry")

    def tearDown(self):
        models.DummyModel.objects.all().delete()
        cache.clear()

    def test_first_pass_returns_result(self):
        results = self.job.get('Alan')
        self.assertEqual(1, len(results))

    def test_only_one_database_query(self):
        with self.assertNumQueries(1):
            for _ in xrange(10):
                self.job.get('Alan')


class TestFilterQuerySetJob(TestCase):

    def setUp(self):
        self.job = QuerySetFilterJob(models.DummyModel)
        models.DummyModel.objects.create(name="Alan")
        models.DummyModel.objects.create(name="Barry")

    def tearDown(self):
        models.DummyModel.objects.all().delete()
        cache.clear()

    def test_first_pass_returns_result(self):
        results = self.job.get(name='Alan')
        self.assertEqual(1, len(results))


class TestGetQuerySetJob(TestCase):

    def setUp(self):
        self.job = QuerySetGetJob(models.DummyModel)
        models.DummyModel.objects.create(name="Alan")
        models.DummyModel.objects.create(name="Barry")

    def tearDown(self):
        models.DummyModel.objects.all().delete()
        cache.clear()

    def test_first_pass_returns_result(self):
        result = self.job.get(name='Alan')
        self.assertEqual('Alan', result.name)


class EchoJob(Job):
    def fetch(self, *args, **kwargs):
        return (args, kwargs)


class TestEchoJob(TestCase):

    def setUp(self):
        self.job = EchoJob()

    def tearDown(self):
        cache.clear()

    def test_unhashable_arg_raises_exception(self):
        with self.assertRaises(RuntimeError):
            self.job.get({})

    def test_unhashable_kwarg_raises_exception(self):
        with self.assertRaises(RuntimeError):
            self.job.get(name={})


