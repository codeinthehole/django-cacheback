puppet:
	puppet module install --target-dir sandbox/puppet/modules/ puppetlabs-rabbitmq -v 2.0.1
	git clone git://github.com/uggedal/puppet-module-python.git sandbox/puppet/modules/python