#!/bin/bash

#Dump Initial data: ./manage.py dumpdata auth sites robots dashboard annotation.kindofoffence > project/fixtures/initial_data.json
#Backup: ./manage.py dumpdata > project/fixtures/initial_data.json

rm */migrations/0*

./manage.py makemigrations

./manage.py migrate

./manage.py loaddata project/fixtures/initial_data.json

./manage.py runserver
