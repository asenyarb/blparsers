#!/bin/sh


./docker-startup/wait-for-db.sh db
python manage.py migrate
celery multi start -A blbackend vkparser@%h --logfile=/usr/src/app/logs/vkparser_logs.txt\
 telegram@%h --logfile=/usr/src/app/logs/telegram_logs.txt -l info -Q:telegram telegram_channel
#celery -A blbackend worker -l info
celery -A blbackend beat -l info --pidfile=