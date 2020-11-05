.PHONY: correct tests

correct:
	poetry run isort cacheback tests
	poetry run black -q cacheback tests

pytests:
	@PYTHONPATH=$(CURDIR):${PYTHONPATH} poetry run pytest

tests:
	@PYTHONPATH=$(CURDIR):${PYTHONPATH} poetry run pytest --cov --isort --flake8 --black

coverage-html: tests
	poetry run coverage html
