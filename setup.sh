#!/bin/bash

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-dev python3-setuptools
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

virtualenv -p python3 venv
source venv/bin/activate
pip install -r project/requirements/main.txt

cat /dev/urandom | tr -cd '!@#$%^&*(-_=+)a-z0-9' | head -c 50 > project/secret_key.txt

sh resetdb.sh
