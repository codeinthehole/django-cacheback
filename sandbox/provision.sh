#!/bin/bash

apt-get update

# Configure rabbit
apt-get install -y rabbitmq-server 
rabbitmqctl add_user cb_rabbit_user somepasswordhere
rabbitmqctl set_permissions cb_rabbit_user ".*" ".*" ".*"

# Other services
apt-get install -y memcached

# Install python deps
apt-get install -y python-pip git
pip install -U pip

# Set-up sandbox
cd /vagrant
make sandbox

# Load fixture data
cd /vagrant/sandbox
./manage.py loaddata fixture.json
