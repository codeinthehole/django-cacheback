develop:
	python setup.py develop
	pip install -r sandbox_requirements.txt
	pip install -r test_requirements.txt

test:
	python setup.py develop
	pip install -r test_requirements.txt

release:
	python setup.py sdist upload
	git push --tags
