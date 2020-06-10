FROM python:3.8.3-alpine3.12

RUN apk add postgresql-dev build-base

WORKDIR /usr/src/app/

ENV DJANGO_SETTINGS_MODULE=blbackend.settings.local_settings
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .