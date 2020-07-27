#!/bin/sh

celery -A blbackend flower --address=0.0.0.0 --port=5555 --pidfile=