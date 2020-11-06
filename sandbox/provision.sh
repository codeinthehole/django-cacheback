#!/bin/bash

sudo apt-get update
sudo apt-get install -y redis-server memcached python3-pip git
sudo pip3 install -U pip poetry honcho

cd /vagrant
poetry install
poetry run pip install -r sandbox/requirements.txt

# Create and fill database
cd /vagrant/sandbox
poetry run python manage.py migrate
poetry run python manage.py loaddata fixture.json
