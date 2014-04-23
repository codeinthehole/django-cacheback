develop:
	python setup.py develop
	pip install -r sandbox_requirements.txt
	pip install -r test_requirements.txt

test:
	python setup.py develop
	pip install -r test_requirements.txt

puppet:
	# Install puppet modules required to set-up sandbox server
	puppet module install --target-dir sandbox/puppet/modules/ puppetlabs-rabbitmq -v 2.0.1
	puppet module install --target-dir sandbox/puppet/modules/ saz-memcached -v 2.0.2
	git clone git://github.com/puppetmodules/puppet-module-python.git sandbox/puppet/modules/python
	git clone git://github.com/codeinthehole/puppet-userconfig.git sandbox/puppet/modules/userconfig

release:
	python setup.py sdist upload
	git push --tags
