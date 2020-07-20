#!/bin/sh


./docker-startup/wait-for-db.sh db
python manage.py migrate && celery -A blbackend worker -B -l info