import pytest


@pytest.mark.xfail
class TestFunctionJob:

    def test_init(self):
        assert True is False

    def test_prepare_args(self):
        assert True is False

    def test_fetch(self):
        assert True is False

    def test_fetch_decorated(self):
        assert True is False

    def test_init_kwargs(self):
        assert True is False


@pytest.mark.xfail
class TestQuerySetJob:

    def test_init(self):
        assert True is False

    def test_key(self):
        assert True is False

    def test_get_init_kwargs(self):
        assert True is False


@pytest.mark.xfail
class TestQuerySetGetJob:

    def test_fetch(self):
        assert True is False


@pytest.mark.xfail
class TestQuerySetGetFilterJob:
    def test_fetch(self):
        assert True is False
