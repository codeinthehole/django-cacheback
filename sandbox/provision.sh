#!/bin/bash

apt-get update
apt-get install -y rabbitmq-server memcached python-pip git

pip install -U pip
pip install -r /vagrant/sandbox_requirements.txt
pip install -r /vagrant/test_requirements.txt

# Configure rabbit
rabbitmqctl add_user cb_rabbit_user somepasswordhere
rabbitmqctl set_permissions cb_rabbit_user ".*" ".*" ".*"
