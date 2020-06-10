#!/bin/sh

echo "Apply database migrations"
python manage.py migrate

echo "Starting celery"
celery -A blbackend worker -B -l info