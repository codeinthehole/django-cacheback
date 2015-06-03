install:
	python setup.py develop
	pip install -r requirements.txt

sandbox: install
	pip install -r sandbox/requirements.txt

test: install 
	./runtests.py

release:
	python setup.py sdist upload
	git push --tags

clean:
	find . -name "*.pyc" -delete
	rm -rf *.egg-info dist
