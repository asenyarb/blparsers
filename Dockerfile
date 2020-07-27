FROM python:3.8.3-alpine3.12

RUN apk add --no-cache postgresql-dev build-base postgresql-client linux-headers

WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .