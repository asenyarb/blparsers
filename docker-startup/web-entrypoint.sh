#!/bin/sh


./docker-startup/wait-for-db.sh db
uwsgi --ini ./docker-startup/uwsgi.ini
