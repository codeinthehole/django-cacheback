# Set default path for all Exec tasks
Exec {
	path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
}

# Install rabbitmq - see https://github.com/puppetlabs/puppetlabs-rabbitmq
class {"rabbitmq::server":
    port => '5673',
	delete_guest_user => true
}
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

# Install memcache
class {"memcached":
    max_memory => 64
}

# Install virtualenv and python dependencies
include python::dev
include python::venv
python::venv::isolate { "/var/www/virtualenv": 
	requirements => "/vagrant/requirements.txt"
}

# Install async_cache library
class library {
    exec {"install-async-cache":
	    command => "/var/www/virtualenv/bin/python /vagrant/setup.py develop",
		user => "root",
	}
}

# Get Django set up
class django {
    exec {"syncdb":
	    command => "/var/www/virtualenv/bin/python /vagrant/sandbox/manage.py syncdb --noinput"
	}
}

include library
include django
