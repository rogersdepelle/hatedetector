#!/bin/bash

#Dump Initial data: ./manage.py dumpdata auth sites robots dashboard annotation.kindofoffence web_scraping.domain > project/fixtures/initial_data.json
#Backup: ./manage.py dumpdata > project/fixtures/initial_data.json

source venv/bin/activate

rm project/db.sqlite3 

./manage.py makemigrations

./manage.py migrate

./manage.py loaddata project/fixtures/backup.json

./manage.py runserver
