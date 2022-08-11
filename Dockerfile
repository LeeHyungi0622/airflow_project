FROM python:3.7-slim

COPY ./api /app

WORKDIR /app

RUN pip install -r requirements.txt
