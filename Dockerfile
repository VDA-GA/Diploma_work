FROM python:3.11-slim

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY /requirements.txt /

RUN pip install --upgrade pip \
    && pip install mysqlclient \
    && pip install -r /requirements.txt --no-cache-dir

COPY . .
