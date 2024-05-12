FROM python:3.10.3-slim

WORKDIR /usr/local/app/


COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
