ARG PYTHON_VERSION=3.9-slim-buster

FROM python:${PYTHON_VERSION} as python

USER root

RUN mkdir /app && apt-get update && apt-get install -y
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000