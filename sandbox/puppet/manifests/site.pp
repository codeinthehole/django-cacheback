# Set default path for all Exec tasks
Exec {
	path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
}

node precise64 {
    package {"git-core": ensure => installed }
	include userconfig
	class {"memcached": max_memory => 64 }
	# Rabbitmq - see https://github.com/puppetlabs/puppetlabs-rabbitmq
	class {"rabbitmq::server": }
	rabbitmq_user {"cb_rabbit_user":
		password => "somepasswordhere",
		provider => "rabbitmqctl"
	}
	rabbitmq_user_permissions {"cb_rabbit_user@/":
		configure_permission => ".*",
		read_permission => ".*",
		write_permission => ".*",
		provider => "rabbitmqctl"
	}
	# Python
	$virtualenv = "/var/www/virtualenv"
	include python::dev
	include python::venv
	python::venv::isolate { $virtualenv: 
		requirements => "/vagrant/requirements.txt"
	}
    exec {"install-async-cache":
	    command => "$virtualenv/bin/python /vagrant/setup.py develop",
		require => Python::Venv::Isolate[$virtualenv]
	}
    exec {"syncdb":
	    command => "$virtualenv/bin/python /vagrant/sandbox/manage.py syncdb --noinput",
		require => Python::Venv::Isolate[$virtualenv]
	}
}
