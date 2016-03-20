import pytest


@pytest.mark.xfail
class TestCachebackDecorator:

    def test_job_init(self):
        assert True is False

    def test_miss_no_fetch(self):
        assert True is False

    def test_miss_fetch(self):
        assert True is False

    def test_stale(self):
        assert True is False

    def test_hit(self):
        assert True is False
