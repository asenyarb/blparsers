#!/bin/sh


./entrypoints/wait-for-db.sh db
python manage.py runserver 0.0.0.0:8000