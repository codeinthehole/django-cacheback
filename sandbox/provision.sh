#!/bin/bash

apt-get update
apt-get install -y rabbitmq-server memcached python-pip git

pip install -U pip
cd /vagrant
pip install -e .[celery]
`which pip` install -r requirements.txt -r sandbox/requirements.txt

# Create database
cd /vagrant/sandbox
./manage.py migrate
./manage.py loaddata fixture.json
