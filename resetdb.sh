#!/bin/bash

#Dump Initial data: ./manage.py dumpdata auth sites robots dashboard > project/fixtures/initial_data.json
#Backup: ./manage.py dumpdata > project/fixtures/initial_data.json

source venv/bin/activate

rm project/db.sqlite3 

./manage.py makemigrations

./manage.py migrate

./manage.py loaddata project/fixtures/initial_data.json

./manage.py runserver