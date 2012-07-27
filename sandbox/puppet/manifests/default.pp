# See https://github.com/puppetlabs/puppetlabs-rabbitmq
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