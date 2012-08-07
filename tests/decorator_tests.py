from django.test import TestCase

from cacheback import FunctionJob


def fetch():
    return 1,2,3


def fetch_with_args(*args):
    return args


class TestDecorator(TestCase):

    def setUp(self):
        self.job = FunctionJob()
        self.job.fetch_on_miss = False

    def test_wrapping_argless_function(self):
        self.assertIsNone(self.job.get(fetch))
        self.assertEqual((1,2,3), self.job.get(fetch))

    def test_wrapping_function(self):
        self.assertIsNone(self.job.get(fetch_with_args, 'testing'))
        self.assertEqual(('testing',), self.job.get(fetch_with_args, 'testing'))


class TestUsingConstructorArgs(TestCase):

    def test_passing_lifetime(self):
        job = FunctionJob(300)
        self.assertEqual(300, job.lifetime)