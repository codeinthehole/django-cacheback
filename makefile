.PHONY = install lint test release clean

install:
	pip install -e .[tests]
	pip install -r sandbox/requirements.txt

release:
	python setup.py sdist upload
	python setup.py bdist_wheel --universal upload
	git push --tags

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -exec xargs rm -r
	rm -rf *.egg-info dist
