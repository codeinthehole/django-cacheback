import pytest


@pytest.mark.xfail
class TestGetCache:

    def test_cache_instance(self):
        assert True is False

    def test_signal(self):
        assert True is False


@pytest.mark.xfail
class TestGetJobClass:

    def test_invalid_module(self):
        assert True is False

    def test_invalid_class(self):
        assert True is False


@pytest.mark.xfail
class TestEnqueueTask:

    def test_celery(self):
        assert True is False

    def test_rq(self):
        assert True is False

    def test_unkown(self):
        assert True is False
