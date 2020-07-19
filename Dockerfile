FROM python:3.8.3-alpine3.12

RUN apk add postgresql-dev build-base postgresql-client

WORKDIR /usr/src/app/

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .