# RabbitMQ Puppet Module
This module manages the RabbitMQ Middleware service.

This module has been tested against 2.7.1 and is known to not support
all features against earlier versions.

### Authors
* Jeff McCune <jeff@puppetlabs.com>
* Dan Bode <dan@puppetlabs.com>

## Classes

This module provides its core functionality through two main classes:

### rabbitmq::repo::apt
Sets up an apt repo source for the vendor rabbitmq packages

    class { 'rabbitmq::repo::apt':
      pin    => 900,
      before => Class['rabbitmq::server']
    }

### rabbitmq::server
Class for installing rabbitmq-server:

    class { 'rabbitmq::server':
      port              => '5673',
      delete_guest_user => true,
    }


## Native Types

**NOTE:** Unfortunately, you must specify the provider explicitly for these types

### rabbitmq_user

query all current users: `$ puppet resource rabbitmq_user`

    rabbitmq_user { 'dan':
      admin    => true,
      password => 'bar',
      provider => 'rabbitmqctl',
    }

### rabbitmq_vhost

query all current vhosts: `$ puppet resource rabbitmq_vhost`

    rabbitmq_vhost { 'myhost':
      ensure => present,
      provider => 'rabbitmqctl',
    }

### rabbitmq\_user\_permissions

    rabbitmq_user_permissions { 'dan@myhost':
      configure_permission => '.*',
      read_permission      => '.*',
      write_permission     => '.*',
      provider => 'rabbitmqctl',
    }

### rabbitmq_plugin

query all currently enabled plugins `$ puppet resource rabbitmq_plugin`

    rabbitmq_plugin {'rabbitmq_stomp':
      ensure => present,
      provider => 'rabbitmqplugins',
    }
