#!/bin/bash

apt-get update
apt-get install -y rabbitmq-server redis-server memcached python-pip git

pip install -U pip honcho
cd /vagrant
pip install -e .[celery]
pip install -e .[rq]
`which pip` install -r requirements.txt -r sandbox/requirements.txt

# Create database
cd /vagrant/sandbox
./manage.py migrate
./manage.py loaddata fixture.json
