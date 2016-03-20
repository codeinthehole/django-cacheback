import pytest
from django.test import TestCase

from cacheback.decorators import cacheback
from cacheback.function import FunctionJob


def fetch():
    return 1, 2, 3


def fetch_with_args(*args):
    return args


class TestDecorator(TestCase):

    @pytest.mark.xfail
    def test_wrapping_argless_function(self):
        decorated_fetch = cacheback(fetch_on_miss=False)(fetch)
        self.assertIsNone(decorated_fetch())
        self.assertEqual((1, 2, 3), decorated_fetch())

    @pytest.mark.xfail
    def test_wrapping_function(self):
        decorated_fetch_with_args = (
            cacheback(fetch_on_miss=False)(fetch_with_args))
        self.assertIsNone(decorated_fetch_with_args('testing'))
        self.assertEqual(('testing',), decorated_fetch_with_args('testing'))


class TestUsingConstructorArgs(TestCase):

    def test_passing_lifetime(self):
        job = FunctionJob(300)
        self.assertEqual(300, job.lifetime)


class CustomFunctionJob(FunctionJob):
    def __init__(self, custom_param=None, *args, **kwargs):
        super(CustomFunctionJob, self).__init__(*args, **kwargs)
        self.custom_param = custom_param

    def fetch(self, *args, **kwargs):
        item = super(CustomFunctionJob, self).fetch(*args, **kwargs)

        return item, self.custom_param

    def get_constructor_kwargs(self):
        kwargs = super(CustomFunctionJob, self).get_constructor_kwargs()
        kwargs['custom_param'] = self.custom_param

        return kwargs


class TestUsingCustomJobClass(TestCase):

    @pytest.mark.xfail
    def test_passing_job_class(self):
        decorated_fetch = (cacheback(
            fetch_on_miss=False,
            job_class=CustomFunctionJob,
            custom_param=200)(fetch))
        self.assertIsNone(decorated_fetch())
        self.assertEqual(((1, 2, 3), 200), decorated_fetch())

    def test_passing_job_class_params(self):
        self.assertRaisesMessage(
            TypeError,
            "__init__() got an unexpected keyword argument 'unknown_param'",
            cacheback,
            job_class=CustomFunctionJob,
            custom_param=200,
            unknown_param=100)
