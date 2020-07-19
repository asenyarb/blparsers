#!/bin/sh


./entrypoints/wait-for-db.sh db
python manage.py migrate && celery -A blbackend worker -B -l info